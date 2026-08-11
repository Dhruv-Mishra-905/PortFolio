import json
import os
import re
from copy import deepcopy
from pathlib import Path

from werkzeug.utils import secure_filename

from experience_data import EXPERIENCES as DEFAULT_EXPERIENCES
from projects_data import PROJECTS as DEFAULT_PROJECTS


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "src" / "uploads"
CONTENT_FILE = DATA_DIR / "portfolio_content.json"

ADMIN_SESSION_KEY = "portfolio_admin_logged_in"

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp"}
ALLOWED_CV_EXTENSIONS = {"pdf", "doc", "docx"}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | {"mp4", "webm", "mov", "m4v"}
ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx"}


DEFAULT_SITE = {
    "name": "Dhruv Mishra",
    "headline": "B.Tech CSE (AI & ML) Student | Web Developer | Python Developer",
    "location": "Ranchi, India",
    "about_1": (
        "Software development student with hands-on experience in web development "
        "using React, Python, HTML, CSS, and JavaScript. I build and deploy full-stack "
        "applications integrating REST APIs and OpenCV-based computer vision features."
    ),
    "about_2": (
        "With practical exposure to machine learning and artificial intelligence "
        "techniques, I enjoy turning complex problems into elegant, user-friendly "
        "applications - from healthcare platforms to real-time crypto trackers."
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


DEFAULT_CERTIFICATES = [
    {
        "slug": "sih-2025",
        "title": "Smart India Hackathon 2025",
        "issuer": "Internal Round - Round 2 Qualifier",
        "description": "Advanced to Round 2 with Face Recognition System project.",
        "skills": ["Python", "OpenCV", "Teamwork"],
        "image_url": "",
        "link_url": "https://github.com/Dhruv-Mishra-905/Python-Projects/tree/main/Learning/Face-Recognise",
        "link_label": "View Project",
    },
    {
        "slug": "edc-college-competition",
        "title": "EDC College Competition",
        "issuer": "Entrepreneurship Development Cell",
        "description": "Led EverHeal team to Round 2 in the college-level EDC competition.",
        "skills": ["Leadership", "Frontend", "Pitching"],
        "image_url": "",
        "link_url": "https://everheal.netlify.app/",
        "link_label": "View Project",
    },
    {
        "slug": "snac-internship",
        "title": "SNAC Internship",
        "issuer": "Smart Network Analytics Center, Usha Martin",
        "description": "Software Development Intern - network analytics dashboard development.",
        "skills": ["JavaScript", "Analytics", "Dashboard"],
        "image_url": "",
        "link_url": "https://github.com/Dhruv-Mishra-905/Main-Projects/tree/641abd0128d91461cc36044abcb8a4cb42b2fdb0/Smart%20Network%20Analytics%20Center%20(SNAC)/Smart%20Network%20Analytics%20Center%20(SNAC)",
        "link_label": "View Work",
    },
    {
        "slug": "svms-internship",
        "title": "SVMS Internship",
        "issuer": "Central Coalfields Limited - Ranchi",
        "description": "Software Development Intern - Society Visitor Management System.",
        "skills": ["React", "Node.js", "MySQL"],
        "image_url": "",
        "link_url": "https://society-visitor-management-system.onrender.com/",
        "link_label": "View Live",
    },
]


DEFAULT_JOURNEY_STEPS = [
    {
        "slug": "early-stage",
        "icon": "🎓",
        "title": "Early Stage",
        "period": "Class 9 — Class 11",
        "description": "Started my programming journey with basic fundamentals and exploring how code works.",
        "tech": ["Python", "HTML", "C/C++", "Pydroid"],
        "highlight": False,
    },
    {
        "slug": "beginner",
        "icon": "📈",
        "title": "Beginner Level",
        "period": "Class 12 — B.Tech 1st Year",
        "description": "Learned web development basics and strengthened core programming with structured practice.",
        "tech": ["HTML/CSS", "C", "Python", "Java", "VS Code"],
        "highlight": False,
    },
    {
        "slug": "intermediate",
        "icon": "🔧",
        "title": "Intermediate Level",
        "period": "1st Year — 2nd Year",
        "description": "Built real projects, explored mobile & computer vision, and started competitive programming.",
        "tech": ["JavaScript", "Bootstrap", "Kotlin", "OpenCV", "Git/GitHub"],
        "highlight": False,
    },
    {
        "slug": "advanced",
        "icon": "🚀",
        "title": "Advanced Level",
        "period": "2nd Year",
        "description": "Focused on full-stack web apps, databases, and deploying scalable real-world solutions.",
        "tech": ["React/Vite", "Node.js", "MySQL", "LeetCode", "CodeChef"],
        "highlight": False,
    },
    {
        "slug": "professional",
        "icon": "⚡",
        "title": "Professional Level",
        "period": "3rd Year — Present",
        "description": "Building production-ready full-stack apps with backend APIs, internships, and AI/ML integrations.",
        "tech": ["ExpressJS", "Flask", "REST API", "SQLite", "AI & ML"],
        "highlight": True,
    },
]


DEFAULT_SKILL_CATEGORIES = [
    {
        "slug": "web-technologies",
        "title": "Web Technologies",
        "icon": "🌐",
        "subtitle": "Frontend & backend web development stack",
        "description": "Technologies I use to build responsive, interactive web applications — from static pages to full-stack apps with REST APIs.",
        "skills": [
            {"name": "HTML", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg", "dot": ""},
            {"name": "CSS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg", "dot": ""},
            {"name": "Bootstrap", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg", "dot": ""},
            {"name": "JavaScript", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg", "dot": ""},
            {"name": "React JS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg", "dot": ""},
            {"name": "Vite", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vitejs/vitejs-original.svg", "dot": ""},
            {"name": "Node JS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg", "dot": ""},
            {"name": "ExpressJS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg", "dot": ""},
            {"name": "Flask", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg", "dot": ""},
            {"name": "REST API", "icon": "", "dot": "🔗"},
        ],
    },
    {
        "slug": "programming-languages",
        "title": "Programming Languages",
        "icon": "</>",
        "subtitle": "Core languages for software development",
        "description": "Languages I've learned and used across web development, mobile apps, competitive programming, and computer vision projects.",
        "skills": [
            {"name": "Python", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", "dot": ""},
            {"name": "Java", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg", "dot": ""},
            {"name": "C", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg", "dot": ""},
            {"name": "Kotlin", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg", "dot": ""},
            {"name": "JavaScript", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg", "dot": ""},
        ],
    },
    {
        "slug": "tools-ides",
        "title": "Tools & IDEs",
        "icon": "🔧",
        "subtitle": "Development environment & productivity tools",
        "description": "Editors, IDEs, and tools I rely on daily for coding, testing APIs, version control, and building applications.",
        "skills": [
            {"name": "VS Code", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg", "dot": ""},
            {"name": "Jupyter Notebook", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg", "dot": ""},
            {"name": "Dev C++", "icon": "", "dot": "⚡"},
            {"name": "Android Studio", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/androidstudio/androidstudio-original.svg", "dot": ""},
            {"name": "Postman", "icon": "", "dot": "📮"},
            {"name": "Git/GitHub", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg", "dot": ""},
            {"name": "Cursor", "icon": "", "dot": "✨"},
            {"name": "Apache Server", "icon": "", "dot": "🌐"},
        ],
    },
    {
        "slug": "databases-others",
        "title": "Databases & Others",
        "icon": "🗄️",
        "subtitle": "Data storage, vision & competitive platforms",
        "description": "Database systems, computer vision libraries, and platforms where I practice algorithms and sharpen problem-solving skills.",
        "skills": [
            {"name": "MySQL", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg", "dot": ""},
            {"name": "SQLite", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg", "dot": ""},
            {"name": "OpenCV", "icon": "", "dot": "👁️"},
            {"name": "LeetCode", "icon": "", "dot": "🏆"},
            {"name": "CodeChef", "icon": "", "dot": "🍽️"},
        ],
    },
]


DEFAULT_ACHIEVEMENTS = [
    {
        "slug": "sih-r2",
        "number": "R2",
        "title": "Smart India Hackathon 2025",
        "description": "Advanced to Round 2 with Face Recognition System",
    },
    {
        "slug": "edc-r2",
        "number": "R2",
        "title": "EDC College Competition",
        "description": "Led EverHeal team to Round 2",
    },
    {
        "slug": "coding-problems",
        "number": "50+",
        "title": "Coding Problems Solved",
        "description": "Across LeetCode and CodeChef platforms",
    },
    {
        "slug": "real-projects",
        "number": "5+",
        "title": "Real-World Projects",
        "description": "Built and deployed web & Python applications",
    },
]


def _project_defaults():
    projects = []
    for project in DEFAULT_PROJECTS.values():
        item = deepcopy(project)
        item.setdefault("image_url", "")
        item.setdefault("bg_media_url", "")
        item.setdefault("description", item.get("summary", ""))
        item.setdefault("skills_learned", item.get("tech", []))
        projects.append(item)
    return projects


def _experience_defaults():
    experiences = []
    for experience in DEFAULT_EXPERIENCES.values():
        item = deepcopy(experience)
        item.setdefault("record_file_url", "")
        item.setdefault("report_file_url", "")
        item.setdefault("report_image_url", "")
        item.setdefault("certificate_image_url", "")
        experiences.append(item)
    return experiences


def default_content():
    return {
        "site": deepcopy(DEFAULT_SITE),
        "projects": _project_defaults(),
        "experiences": _experience_defaults(),
        "certificates": deepcopy(DEFAULT_CERTIFICATES),
        "journey": deepcopy(DEFAULT_JOURNEY_STEPS),
        "skills": deepcopy(DEFAULT_SKILL_CATEGORIES),
        "achievements": deepcopy(DEFAULT_ACHIEVEMENTS),
    }


def load_content():
    if not CONTENT_FILE.exists():
        return default_content()

    with CONTENT_FILE.open("r", encoding="utf-8") as handle:
        saved = json.load(handle)

    content = default_content()
    if "site" in saved:
        content["site"].update(saved["site"])
    for key in ("projects", "experiences", "certificates", "journey", "skills", "achievements"):
        if key in saved:
            content[key] = saved[key]
    return content


def save_content(content):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with CONTENT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(content, handle, indent=2, ensure_ascii=False)


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


def save_uploaded_file(file_storage, allowed_extensions, old_value=""):
    if not file_storage or not file_storage.filename:
        return old_value

    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in allowed_extensions:
        return old_value

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    base = slugify(filename.rsplit(".", 1)[0], "upload")
    stored_name = f"{base}.{extension}"
    target = UPLOAD_DIR / stored_name
    counter = 2
    while target.exists():
        stored_name = f"{base}-{counter}.{extension}"
        target = UPLOAD_DIR / stored_name
        counter += 1

    file_storage.save(target)
    return f"/src/uploads/{stored_name}"


def save_uploaded_image(file_storage, old_value=""):
    return save_uploaded_file(file_storage, ALLOWED_IMAGE_EXTENSIONS, old_value)


def save_uploaded_cv(file_storage, old_value=""):
    return save_uploaded_file(file_storage, ALLOWED_CV_EXTENSIONS, old_value)


def save_uploaded_media(file_storage, old_value=""):
    return save_uploaded_file(file_storage, ALLOWED_MEDIA_EXTENSIONS, old_value)


def save_uploaded_document(file_storage, old_value=""):
    return save_uploaded_file(file_storage, ALLOWED_DOCUMENT_EXTENSIONS, old_value)


def authenticate_admin(name, email):
    site = load_content()["site"]
    return (
        name.strip().lower() == site.get("admin_secret_name", "").strip().lower()
        and email.strip().lower() == site.get("admin_secret_email", "").strip().lower()
    )
