"""Illustrative role profiles for learning, not live jobs or hiring criteria."""


ROLE_PROFILES = (
    {
        "role_id": "python_backend",
        "title": "Python backend developer",
        "skills": ("Python", "FastAPI", "SQL", "Git", "Docker"),
    },
    {
        "role_id": "react_frontend",
        "title": "React frontend developer",
        "skills": ("JavaScript", "React", "HTML", "CSS", "Git"),
    },
    {
        "role_id": "java_backend",
        "title": "Java backend developer",
        "skills": ("Java", "Spring Boot", "SQL", "Git", "Docker"),
    },
    {
        "role_id": "python_data_analysis",
        "title": "Python data analyst",
        "skills": ("Python", "SQL", "Pandas", "NumPy", "Git"),
    },
)


def match_roles(skills: list[str]) -> list[dict]:
    """Rank positive overlaps with canonical skills; duplicates carry no weight."""
    detected = set(skills)
    results = []
    for profile in ROLE_PROFILES:
        profile_skills = set(profile["skills"])
        matched = detected & profile_skills
        if not matched:
            continue
        results.append({
            "role_id": profile["role_id"],
            "title": profile["title"],
            "skill_overlap_percent": round(100 * len(matched) / len(profile_skills), 1),
            "matched_skills": sorted(matched, key=str.casefold),
            "not_detected_skills": sorted(profile_skills - detected, key=str.casefold),
        })
    return sorted(results, key=lambda result: (-result["skill_overlap_percent"], result["role_id"]))
