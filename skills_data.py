from portfolio_store import load_content


def get_skill_category(slug):
    categories = load_content().get("skills", [])
    return next((c for c in categories if c.get("slug") == slug), None)


def get_all_skill_categories():
    return load_content().get("skills", [])
