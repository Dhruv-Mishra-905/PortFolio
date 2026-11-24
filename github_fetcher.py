import base64
import re
import urllib.error
import urllib.request
from functools import lru_cache

import markdown


GITHUB_API = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"


def _api_get(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "DhruvMishra-Portfolio",
        },
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        return resp.read().decode("utf-8")


@lru_cache(maxsize=32)
def fetch_repo_info(owner, repo):
    try:
        data = _api_get(f"{GITHUB_API}/repos/{owner}/{repo}")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return {}

    import json
    info = json.loads(data)
    return {
        "description": info.get("description") or "",
        "stars": info.get("stargazers_count", 0),
        "language": info.get("language") or "",
        "homepage": info.get("homepage") or "",
        "updated_at": info.get("updated_at", ""),
        "topics": info.get("topics") or [],
    }


def _readme_candidates(readme_path):
    if readme_path:
        return [
            f"{readme_path}/README.md",
            f"{readme_path}/readme.md",
            f"{readme_path}/Readme.md",
        ]
    return ["README.md", "readme.md", "Readme.md"]


@lru_cache(maxsize=32)
def fetch_readme_markdown(owner, repo, readme_path="", ref="main"):
    import json

    for candidate in _readme_candidates(readme_path):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{candidate}?ref={ref}"
        try:
            data = json.loads(_api_get(url))
            if data.get("encoding") == "base64" and data.get("content"):
                return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            continue
    return ""


def _resolve_image_url(src, owner, repo, ref, readme_path):
    if not src:
        return src
    if src.startswith(("http://", "https://", "data:")):
        return src
    if src.startswith("//"):
        return "https:" + src

    base_path = readme_path.strip("/") if readme_path else ""
    if src.startswith("/"):
        path = src.lstrip("/")
    elif src.startswith("./"):
        path = f"{base_path}/{src[2:]}" if base_path else src[2:]
    else:
        path = f"{base_path}/{src}" if base_path else src

    path = path.replace("//", "/")
    return f"{RAW_BASE}/{owner}/{repo}/{ref}/{path}"


def _rewrite_markdown_images(md_text, owner, repo, ref, readme_path):
    def replacer(match):
        alt, src = match.group(1), match.group(2)
        resolved = _resolve_image_url(src, owner, repo, ref, readme_path)
        return f"![{alt}]({resolved})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replacer, md_text)


def extract_first_image(md_text, owner, repo, ref, readme_path):
    match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", md_text)
    if not match:
        return None
    return _resolve_image_url(match.group(2), owner, repo, ref, readme_path)


def extract_extra_images(md_text, owner, repo, ref, readme_path, limit=6):
    images = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", md_text):
        url = _resolve_image_url(match.group(2), owner, repo, ref, readme_path)
        if url and url not in images:
            images.append({"alt": match.group(1), "url": url})
        if len(images) >= limit:
            break
    return images


def render_readme_html(md_text, owner, repo, ref, readme_path):
    if not md_text.strip():
        return ""

    md_text = _rewrite_markdown_images(md_text, owner, repo, ref, readme_path)
    html = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    )

    def link_replacer(match):
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        resolved = _resolve_image_url(href, owner, repo, ref, readme_path)
        return f'href="{resolved}"'

    html = re.sub(r'href="([^"]+)"', link_replacer, html)
    return html


def fetch_project_github_data(project):
    owner = project["github_owner"]
    repo = project["github_repo"]
    readme_path = project.get("readme_path", "")
    ref = project.get("ref", "main")

    repo_info = fetch_repo_info(owner, repo)
    readme_md = fetch_readme_markdown(owner, repo, readme_path, ref)
    readme_html = render_readme_html(readme_md, owner, repo, ref, readme_path)
    hero_image = extract_first_image(readme_md, owner, repo, ref, readme_path)
    gallery = extract_extra_images(readme_md, owner, repo, ref, readme_path)

    description = project["summary"]
    if repo_info.get("description"):
        description = repo_info["description"]

    return {
        "repo_info": repo_info,
        "readme_html": readme_html,
        "readme_found": bool(readme_md.strip()),
        "hero_image": hero_image,
        "gallery": gallery,
        "description": description,
    }
