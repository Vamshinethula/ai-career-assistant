"""Small local baseline: detect catalog terms, not proficiency or intent."""

import re


SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "Java": ("java",),
    "JavaScript": ("javascript", "java script"),
    "TypeScript": ("typescript",),
    "C++": ("c++",),
    "C#": ("c#", "c sharp"),
    "HTML": ("html", "html5"),
    "CSS": ("css", "css3"),
    "React": ("react", "react.js", "reactjs"),
    "Angular": ("angular", "angularjs"),
    "Node.js": ("node.js", "nodejs", "node js"),
    "FastAPI": ("fastapi", "fast api"),
    "Django": ("django",),
    "Flask": ("flask",),
    "Spring Boot": ("spring boot", "springboot"),
    "SQL": ("sql",),
    "SQLite": ("sqlite",),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "MongoDB": ("mongodb", "mongo db"),
    "SQLAlchemy": ("sqlalchemy",),
    "Git": ("git",),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure",),
    "Linux": ("linux",),
    "Pandas": ("pandas",),
    "NumPy": ("numpy",),
    "scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "PyTorch": ("pytorch",),
    "TensorFlow": ("tensorflow",),
}


def extract_skills(text: str | None) -> list[str]:
    """Return unique canonical names in alphabetical order for explicit mentions."""
    normalized = " ".join((text or "").casefold().split())
    candidates = []
    for skill, aliases in SKILL_ALIASES.items():
        # Include +/# in the boundaries so punctuation-bearing names stay intact.
        for alias in aliases:
            pattern = r"(?<![\w+#])" + re.escape(alias) + r"(?![\w+#])"
            for match in re.finditer(pattern, normalized):
                candidates.append((match.start(), match.end(), skill))

    # Prefer a complete alias over a shorter skill inside it (Java Script/Java).
    # A separate Java mention remains eligible because its span does not overlap.
    occupied = []
    matches = set()
    for start, end, skill in sorted(candidates, key=lambda item: -(item[1] - item[0])):
        if any(start < used_end and end > used_start for used_start, used_end in occupied):
            continue
        occupied.append((start, end))
        matches.add(skill)
    return sorted(matches, key=str.casefold)
