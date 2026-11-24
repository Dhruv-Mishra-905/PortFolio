from __future__ import annotations

import os
import re
import uuid
from copy import deepcopy

from supabase import create_client, Client
from werkzeug.utils import secure_filename

# ── Supabase client ─────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

_supabase: Client | None = None


def _sb() -> Client:
    """Lazy-init Supabase client. Raises clear error if env vars missing."""
    global _supabase
    if _supabase is None:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        if not url or not key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY env vars are not set. "
                "Add them in your Render dashboard under Environment Variables."
            )
        _supabase = create_client(url, key)
    return _supabase


ADMIN_SESSION_KEY = "portfolio_admin_logged_in"

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp"}
ALLOWED_CV_EXTENSIONS = {"pdf", "doc", "docx"}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | {"mp4", "webm", "mov", "m4v"}
ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx"}

# ── Default fallback data (kept for hard-coded journey / skills pages) ──

DEFAULT_SITE = {
    "name": "Dhruv Mishra",
    "headline": "B.Tech CSE (AI & ML) Student | Web Developer | Python Developer",
    "location": "Ranchi, India",
    "about_1": (
        "Software development student with hands-on experience in web development "
        "using React, Python, HTML, CSS, and JavaScript. Built and deployed full-stack "
        "applications integrating REST APIs and OpenCV-based computer vision features, "
        "with practical exposure to machine learning and artificial intelligence techniques."
    ),
    "about_2": (
        "Currently pursuing B.Tech in Computer Science Engineering (AI & ML) at "
        "Aditya College of Engineering & Technology (JNTUK). I enjoy turning complex "
        "problems into elegant, user-friendly applications — from healthcare platforms "
        "to real-time crypto trackers."
    ),
    "email": "dhruvmh50@gmail.com",
    "phone": "+91 6204282905",
    "languages": "Hindi, English",
    "projects_count": "5+",
    "problems_count": "50+",
    "internships_count": "2",
    "cv_label": "View CV",
    "cv_url": "",
    "contact_intro": (
        "I'm always open to discussing new projects, internship opportunities, "
        "or collaborations."
    ),
    "admin_secret_name": os.environ.get("PORTFOLIO_ADMIN_NAME", "Dhruv Admin"),
    "admin_secret_email": os.environ.get("PORTFOLIO_ADMIN_EMAIL", "dhruv@admin.local"),
}


# ── Supabase helpers ────────────────────────────────────────

def _row_to_dict(row: dict) -> dict:
    """Strip internal DB columns from a row for template consumption."""
    out = dict(row)
    for key in ("id", "sort_order", "created_at", "updated_at"):
        out.pop(key, None)
    return out


def _load_site() -> dict:
    """Fetch the single site-settings row (or return defaults)."""
    try:
        resp = _sb().table("site").select("*").eq("id", 1).execute()
        if resp.data:
            row = _row_to_dict(resp.data[0])
            merged = deepcopy(DEFAULT_SITE)
            merged.update({k: v for k, v in row.items() if v is not None and v != ""})
            return merged
    except Exception as e:
        print(f"[portfolio_store] Supabase error loading site: {e}")
    return deepcopy(DEFAULT_SITE)


def _load_projects() -> list[dict]:
    try:
        resp = _sb().table("projects").select("*").order("sort_order").execute()
        return [_row_to_dict(r) for r in resp.data] if resp.data else []
    except Exception as e:
        print(f"[portfolio_store] Supabase error loading projects: {e}")
        return []


def _load_experiences() -> list[dict]:
    try:
        resp = _sb().table("experiences").select("*").order("sort_order").execute()
        return [_row_to_dict(r) for r in resp.data] if resp.data else []
    except Exception as e:
        print(f"[portfolio_store] Supabase error loading experiences: {e}")
        return []


def _load_certificates() -> list[dict]:
    try:
        resp = _sb().table("certificates").select("*").order("sort_order").execute()
        return [_row_to_dict(r) for r in resp.data] if resp.data else []
    except Exception as e:
        print(f"[portfolio_store] Supabase error loading certificates: {e}")
        return []


# ── Public API (matches the old interface) ──────────────────

def load_content() -> dict:
    return {
        "site": _load_site(),
        "projects": _load_projects(),
        "experiences": _load_experiences(),
        "certificates": _load_certificates(),
    }


def save_content(content: dict):
    """Persist the full content dict back to Supabase."""
    sb = _sb()

    # Site
    if "site" in content:
        site_data = {k: v for k, v in content["site"].items() if k != "id"}
        sb.table("site").upsert({"id": 1, **site_data}).execute()

    # Projects — full replace strategy: delete all, re-insert
    if "projects" in content:
        sb.table("projects").delete().neq("id", 0).execute()
        for idx, proj in enumerate(content["projects"]):
            row = {k: v for k, v in proj.items() if k not in ("id", "created_at", "updated_at")}
            row["sort_order"] = idx
            row.setdefault("slug", slugify(row.get("title", "project")))
            sb.table("projects").insert(row).execute()

    # Experiences — full replace
    if "experiences" in content:
        sb.table("experiences").delete().neq("id", 0).execute()
        for idx, exp in enumerate(content["experiences"]):
            row = {k: v for k, v in exp.items() if k not in ("id", "created_at", "updated_at")}
            row["sort_order"] = idx
            row.setdefault("slug", slugify(row.get("company", "experience")))
            sb.table("experiences").insert(row).execute()

    # Certificates — full replace
    if "certificates" in content:
        sb.table("certificates").delete().neq("id", 0).execute()
        for idx, cert in enumerate(content["certificates"]):
            row = {k: v for k, v in cert.items() if k not in ("id", "created_at", "updated_at")}
            row["sort_order"] = idx
            row.setdefault("slug", slugify(row.get("title", "certificate")))
            sb.table("certificates").insert(row).execute()


# ── Slug helpers ────────────────────────────────────────────

def slugify(value, fallback="item"):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def split_list(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def unique_slug(items, title, current_slug=None):
    base = slugify(title)
    used = {item.get("slug") for item in items if item.get("slug") != current_slug}
    slug = current_slug or base
    if slug not in used:
        return slug
    index = 2
    while f"{base}-{index}" in used:
        index += 1
    return f"{base}-{index}"


# ── File upload helpers (Supabase Storage) ──────────────────

def _upload_to_storage(file_storage, allowed_extensions, old_value=""):
    """Upload a file to Supabase Storage bucket 'uploads'."""
    if not file_storage or not file_storage.filename:
        return old_value

    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in allowed_extensions:
        return old_value

    base = slugify(filename.rsplit(".", 1)[0], "upload")
    stored_name = f"{base}-{uuid.uuid4().hex[:8]}.{extension}"
    file_bytes = file_storage.read()

    try:
        _sb().storage.from_("uploads").upload(
            path=stored_name,
            file=file_bytes,
            file_options={"content-type": file_storage.content_type or "application/octet-stream"},
        )
        public_url = _sb().storage.from_("uploads").get_public_url(stored_name)
        return public_url
    except Exception:
        return old_value


def save_uploaded_image(file_storage, old_value=""):
    return _upload_to_storage(file_storage, ALLOWED_IMAGE_EXTENSIONS, old_value)


def save_uploaded_cv(file_storage, old_value=""):
    return _upload_to_storage(file_storage, ALLOWED_CV_EXTENSIONS, old_value)


def save_uploaded_media(file_storage, old_value=""):
    return _upload_to_storage(file_storage, ALLOWED_MEDIA_EXTENSIONS, old_value)


def save_uploaded_document(file_storage, old_value=""):
    return _upload_to_storage(file_storage, ALLOWED_DOCUMENT_EXTENSIONS, old_value)


# ── Admin auth ──────────────────────────────────────────────

def authenticate_admin(name, email):
    site = load_content()["site"]
    return (
        name.strip().lower() == site.get("admin_secret_name", "").strip().lower()
        and email.strip().lower() == site.get("admin_secret_email", "").strip().lower()
    )
