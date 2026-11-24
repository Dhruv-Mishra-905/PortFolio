SKILL_CATEGORIES = {
    "web-technologies": {
        "slug": "web-technologies",
        "title": "Web Technologies",
        "icon": "🌐",
        "subtitle": "Frontend & backend web development stack",
        "description": "Technologies I use to build responsive, interactive web applications — from static pages to full-stack apps with REST APIs.",
        "skills": [
            {"name": "HTML", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"},
            {"name": "CSS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"},
            {"name": "Bootstrap", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg"},
            {"name": "JavaScript", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"},
            {"name": "React JS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"},
            {"name": "Vite", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vitejs/vitejs-original.svg"},
            {"name": "Node JS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg"},
            {"name": "ExpressJS", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg"},
            {"name": "Flask", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg"},
            {"name": "REST API", "dot": "🔗"},
        ],
    },
    "programming-languages": {
        "slug": "programming-languages",
        "title": "Programming Languages",
        "icon": "</>",
        "subtitle": "Core languages for software development",
        "description": "Languages I've learned and used across web development, mobile apps, competitive programming, and computer vision projects.",
        "skills": [
            {"name": "Python", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"},
            {"name": "Java", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg"},
            {"name": "C", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg"},
            {"name": "Kotlin", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg"},
            {"name": "JavaScript", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"},
        ],
    },
    "tools-ides": {
        "slug": "tools-ides",
        "title": "Tools & IDEs",
        "icon": "🔧",
        "subtitle": "Development environment & productivity tools",
        "description": "Editors, IDEs, and tools I rely on daily for coding, testing APIs, version control, and building applications.",
        "skills": [
            {"name": "VS Code", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg"},
            {"name": "Jupyter Notebook", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg"},
            {"name": "Dev C++", "dot": "⚡"},
            {"name": "Android Studio", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/androidstudio/androidstudio-original.svg"},
            {"name": "Postman", "dot": "📮"},
            {"name": "Git/GitHub", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg"},
            {"name": "Cursor", "dot": "✨"},
            {"name": "Apache Server", "dot": "🌐"},
        ],
    },
    "databases-others": {
        "slug": "databases-others",
        "title": "Databases & Others",
        "icon": "🗄️",
        "subtitle": "Data storage, vision & competitive platforms",
        "description": "Database systems, computer vision libraries, and platforms where I practice algorithms and sharpen problem-solving skills.",
        "skills": [
            {"name": "MySQL", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg"},
            {"name": "SQLite", "icon": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg"},
            {"name": "OpenCV", "dot": "👁️"},
            {"name": "LeetCode", "dot": "🏆"},
            {"name": "CodeChef", "dot": "🍽️"},
        ],
    },
}


def get_skill_category(slug):
    return SKILL_CATEGORIES.get(slug)


def get_all_skill_categories():
    return list(SKILL_CATEGORIES.values())
