import os

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from github_fetcher import fetch_project_github_data
from journey_data import get_journey_steps
from portfolio_store import (
    ADMIN_SESSION_KEY,
    authenticate_admin,
    load_content,
    save_content,
    save_uploaded_cv,
    save_uploaded_document,
    save_uploaded_image,
    save_uploaded_media,
    split_list,
    unique_slug,
)
from skills_data import get_all_skill_categories, get_skill_category

app = Flask(
    __name__,
    template_folder='components',
    static_folder='src',
    static_url_path='/src',
)
app.secret_key = os.environ.get('PORTFOLIO_SECRET_KEY', 'change-this-portfolio-admin-secret')


def _content():
    return load_content()


def _projects():
    return _content()["projects"]


def _project(slug):
    return next((project for project in _projects() if project.get("slug") == slug), None)


def _featured_projects():
    return [project for project in _projects() if project.get("featured")]


def _experiences():
    return _content()["experiences"]


def _experience(slug):
    return next((experience for experience in _experiences() if experience.get("slug") == slug), None)


def _admin_required():
    if not session.get(ADMIN_SESSION_KEY):
        return redirect(url_for("home"))
    return None


@app.route('/')
def home():
    content = _content()
    return render_template(
        'index.html',
        site=content["site"],
        journey_steps=get_journey_steps(),
        skill_categories=get_all_skill_categories(),
        experiences=content["experiences"],
        featured_projects=[p for p in content["projects"] if p.get("featured")],
        certificates=content["certificates"],
        achievements=content["achievements"],
    )


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=_projects())


@app.route('/projects/<slug>')
def project_detail(slug):
    project = _project(slug)
    if not project:
        abort(404)
    github_data = fetch_project_github_data(project)
    return render_template('project_detail.html', project=project, github=github_data)


@app.route('/experience/<slug>')
def experience_detail(slug):
    experience = _experience(slug)
    if not experience:
        abort(404)
    return render_template('experience_detail.html', experience=experience)


@app.route('/skills/<slug>')
def skill_detail(slug):
    category = get_skill_category(slug)
    if not category:
        abort(404)
    return render_template('skill_detail.html', category=category)


@app.route('/hidden-admin-check', methods=['POST'])
def hidden_admin_check():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    if authenticate_admin(name, email):
        session[ADMIN_SESSION_KEY] = True
        return redirect(url_for("admin_dashboard"))
    return redirect("https://formspree.io/f/mgovkenr", code=307)


@app.route('/dhruv-control-panel')
def admin_dashboard():
    blocked = _admin_required()
    if blocked:
        return blocked
    return render_template('admin.html', content=_content())


@app.route('/dhruv-control-panel/site', methods=['POST'])
def admin_update_site():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    for key in content["site"]:
        content["site"][key] = request.form.get(key, content["site"][key])
    content["site"]["cv_url"] = save_uploaded_cv(request.files.get("cv_file"), content["site"].get("cv_url", ""))
    save_content(content)
    flash("Main page details updated.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/projects/save', methods=['POST'])
def admin_save_project():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    projects = content["projects"]
    current_slug = request.form.get("current_slug", "")
    project = next((item for item in projects if item.get("slug") == current_slug), None)

    if project is None:
        project = {}
        projects.append(project)

    title = request.form.get("title", "Untitled Project").strip() or "Untitled Project"
    project.update({
        "slug": unique_slug(projects, title, current_slug or None),
        "title": title,
        "icon": request.form.get("icon", "[]"),
        "icon_class": request.form.get("icon_class", "project-icon--health"),
        "role": request.form.get("role", ""),
        "date": request.form.get("date", ""),
        "summary": request.form.get("summary", ""),
        "description": request.form.get("description", request.form.get("summary", "")),
        "skills_learned": split_list(request.form.get("skills_learned", "")),
        "tech": split_list(request.form.get("tech", "")),
        "github_url": request.form.get("github_url") or None,
        "live_url": request.form.get("live_url") or None,
        "github_owner": request.form.get("github_owner", ""),
        "github_repo": request.form.get("github_repo", ""),
        "readme_path": request.form.get("readme_path", ""),
        "ref": request.form.get("ref", "main"),
        "featured": request.form.get("featured") == "on",
    })
    project["image_url"] = save_uploaded_image(request.files.get("image"), project.get("image_url", ""))
    project["bg_media_url"] = save_uploaded_media(request.files.get("bg_media"), project.get("bg_media_url", ""))

    save_content(content)
    flash("Project saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/projects/<slug>/delete', methods=['POST'])
def admin_delete_project(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["projects"] = [item for item in content["projects"] if item.get("slug") != slug]
    save_content(content)
    flash("Project removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/experiences/save', methods=['POST'])
def admin_save_experience():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    experiences = content["experiences"]
    current_slug = request.form.get("current_slug", "")
    experience = next((item for item in experiences if item.get("slug") == current_slug), None)

    if experience is None:
        experience = {}
        experiences.append(experience)

    company = request.form.get("company", "Untitled Internship").strip() or "Untitled Internship"
    title = request.form.get("title", "Internship").strip() or "Internship"
    experience.update({
        "slug": unique_slug(experiences, company, current_slug or None),
        "title": title,
        "company": company,
        "location": request.form.get("location", ""),
        "date": request.form.get("date", ""),
        "icon": request.form.get("icon", "IN"),
        "summary": request.form.get("summary", ""),
        "tech": split_list(request.form.get("tech", "")),
        "github_url": request.form.get("github_url") or None,
        "live_url": request.form.get("live_url") or None,
        "points": [line.strip() for line in request.form.get("points", "").splitlines() if line.strip()],
        "responsibilities": [line.strip() for line in request.form.get("responsibilities", "").splitlines() if line.strip()],
    })
    experience["record_file_url"] = save_uploaded_document(
        request.files.get("record_file"),
        experience.get("record_file_url", ""),
    )
    experience["report_file_url"] = save_uploaded_document(
        request.files.get("report_file"),
        experience.get("report_file_url", ""),
    )
    experience["report_image_url"] = save_uploaded_image(
        request.files.get("report_image"),
        experience.get("report_image_url", ""),
    )
    experience["certificate_image_url"] = save_uploaded_image(
        request.files.get("certificate_image"),
        experience.get("certificate_image_url", ""),
    )

    save_content(content)
    flash("Internship saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/experiences/<slug>/delete', methods=['POST'])
def admin_delete_experience(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["experiences"] = [item for item in content["experiences"] if item.get("slug") != slug]
    save_content(content)
    flash("Internship removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/certificates/save', methods=['POST'])
def admin_save_certificate():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    certificates = content["certificates"]
    current_slug = request.form.get("current_slug", "")
    certificate = next((item for item in certificates if item.get("slug") == current_slug), None)

    if certificate is None:
        certificate = {}
        certificates.append(certificate)

    title = request.form.get("title", "Untitled Certificate").strip() or "Untitled Certificate"
    certificate.update({
        "slug": unique_slug(certificates, title, current_slug or None),
        "title": title,
        "issuer": request.form.get("issuer", ""),
        "description": request.form.get("description", ""),
        "skills": split_list(request.form.get("skills", "")),
        "link_url": request.form.get("link_url", ""),
        "link_label": request.form.get("link_label", "View Certificate"),
    })
    certificate["image_url"] = save_uploaded_image(request.files.get("image"), certificate.get("image_url", ""))

    save_content(content)
    flash("Certificate saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/certificates/<slug>/delete', methods=['POST'])
def admin_delete_certificate(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["certificates"] = [item for item in content["certificates"] if item.get("slug") != slug]
    save_content(content)
    flash("Certificate removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/journey/save', methods=['POST'])
def admin_save_journey():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    steps = content["journey"]
    current_slug = request.form.get("current_slug", "")
    step = next((s for s in steps if s.get("slug") == current_slug), None)

    if step is None:
        step = {}
        steps.append(step)

    title = request.form.get("title", "New Stage").strip() or "New Stage"
    step.update({
        "slug": unique_slug(steps, title, current_slug or None),
        "icon": request.form.get("icon", "🎓"),
        "title": title,
        "period": request.form.get("period", ""),
        "description": request.form.get("description", ""),
        "tech": split_list(request.form.get("tech", "")),
        "highlight": request.form.get("highlight") == "on",
    })

    save_content(content)
    flash("Journey step saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/journey/<slug>/delete', methods=['POST'])
def admin_delete_journey(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["journey"] = [s for s in content["journey"] if s.get("slug") != slug]
    save_content(content)
    flash("Journey step removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/skills/save', methods=['POST'])
def admin_save_skill_category():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    categories = content["skills"]
    current_slug = request.form.get("current_slug", "")
    category = next((c for c in categories if c.get("slug") == current_slug), None)

    if category is None:
        category = {}
        categories.append(category)

    title = request.form.get("title", "New Category").strip() or "New Category"

    # Parse skills: each line = "Name|icon_url" or just "Name" (uses dot emoji)
    raw_skills = request.form.get("skills_list", "")
    skill_dot = request.form.get("skill_dot", "")
    parsed_skills = []
    for line in raw_skills.splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            name, icon = line.split("|", 1)
            parsed_skills.append({"name": name.strip(), "icon": icon.strip(), "dot": ""})
        else:
            parsed_skills.append({"name": line, "icon": "", "dot": skill_dot})

    category.update({
        "slug": unique_slug(categories, title, current_slug or None),
        "title": title,
        "icon": request.form.get("icon", "🔧"),
        "subtitle": request.form.get("subtitle", ""),
        "description": request.form.get("description", ""),
        "skills": parsed_skills,
    })

    save_content(content)
    flash("Skill category saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/skills/<slug>/delete', methods=['POST'])
def admin_delete_skill_category(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["skills"] = [c for c in content["skills"] if c.get("slug") != slug]
    save_content(content)
    flash("Skill category removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/achievements/save', methods=['POST'])
def admin_save_achievement():
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    achievements = content["achievements"]
    current_slug = request.form.get("current_slug", "")
    achievement = next((a for a in achievements if a.get("slug") == current_slug), None)

    if achievement is None:
        achievement = {}
        achievements.append(achievement)

    title = request.form.get("title", "Achievement").strip() or "Achievement"
    achievement.update({
        "slug": unique_slug(achievements, title, current_slug or None),
        "number": request.form.get("number", ""),
        "title": title,
        "description": request.form.get("description", ""),
    })

    save_content(content)
    flash("Achievement saved.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/achievements/<slug>/delete', methods=['POST'])
def admin_delete_achievement(slug):
    blocked = _admin_required()
    if blocked:
        return blocked

    content = _content()
    content["achievements"] = [a for a in content["achievements"] if a.get("slug") != slug]
    save_content(content)
    flash("Achievement removed.")
    return redirect(url_for("admin_dashboard"))


@app.route('/dhruv-control-panel/logout', methods=['POST'])
def admin_logout():
    session.pop(ADMIN_SESSION_KEY, None)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
