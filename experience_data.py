EXPERIENCES = {
    "snac": {
        "slug": "snac",
        "title": "Software Development Intern",
        "company": "Smart Network Analytics Center (SNAC), Usha Martin",
        "location": "Ranchi, India",
        "date": "May 2026 — Jun 2026",
        "icon": "📡",
        "summary": "Engineered dashboard components for real-time network analytics and data visualization at Usha Martin's SNAC facility.",
        "tech": ["JavaScript", "Data Visualization", "Analytics", "Dashboards"],
        "github_url": "https://github.com/Dhruv-Mishra-905/Main-Projects/tree/641abd0128d91461cc36044abcb8a4cb42b2fdb0/Smart%20Network%20Analytics%20Center%20(SNAC)/Smart%20Network%20Analytics%20Center%20(SNAC)",
        "live_url": None,
        "points": [
            "Engineered dashboard components for real-time network analytics and data visualization, giving the team clearer insight into device performance and connectivity trends.",
            "Analyzed device and traffic data alongside the technical team to strengthen monitoring workflows and surface usage patterns.",
            "Collaborated on UI components that translate complex network metrics into actionable visual summaries for operators.",
        ],
        "responsibilities": [
            "Built and refined analytics dashboard widgets for live network monitoring.",
            "Worked with device and traffic datasets to improve reporting accuracy.",
            "Supported the team in translating technical requirements into frontend features.",
        ],
    },
    "svms": {
        "slug": "svms",
        "title": "Software Development Intern",
        "company": "Society Visitor Management System (SVMS), Central Coalfields Limited",
        "location": "Ranchi, India",
        "date": "Jun 2026 — Jul 2026",
        "icon": "🏢",
        "summary": "Delivered frontend and backend components of a full-stack visitor management system for Central Coalfields Limited.",
        "tech": ["React", "Node.js", "MySQL", "REST API"],
        "github_url": "https://github.com/Dhruv-Mishra-905/Main-Projects/tree/main/SVMS/society-visitor-management-system",
        "live_url": "https://society-visitor-management-system.onrender.com/",
        "points": [
            "Delivered frontend and backend components of a visitor management system, streamlining check-in and record-keeping workflows.",
            "Implemented form handling and dashboard features that improved administrative efficiency and data accuracy.",
            "Built check-in flows and admin dashboards used for day-to-day society visitor operations.",
        ],
        "responsibilities": [
            "Developed React frontend screens for visitor registration and admin dashboards.",
            "Implemented backend APIs and database integration for visitor records.",
            "Deployed and maintained the live application on Render.",
        ],
    },
}


def get_experience(slug):
    return EXPERIENCES.get(slug)


def get_all_experiences():
    return list(EXPERIENCES.values())
