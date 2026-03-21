"""
skill_extractor.py — Rutvi's Task R1
Enhanced skill extraction using keyword matching + alias normalization.
(spaCy-free version — compatible with Python 3.14+)
"""

import json
import os
import re

# ── Alias map: common shorthands → canonical skill name ──────────────────────
ALIASES = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "py": "Python",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "ai": "Artificial Intelligence",
    "cv": "Computer Vision",
    "sql": "SQL",
    "nosql": "MongoDB",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "react": "React",
    "reactjs": "React",
    "vue": "Vue",
    "vuejs": "Vue",
    "angular": "Angular",
    "angularjs": "Angular",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "gcp": "GCP",
    "azure": "Azure",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "pg": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "git": "Git",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "oop": "Object-Oriented Programming",
    "html": "HTML",
    "css": "CSS",
    "scss": "CSS",
    "rest": "REST APIs",
    "restful": "REST APIs",
    "graphql": "GraphQL",
    "excel": "Excel",
    "tableau": "Tableau",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
    "data structures": "Data Structures",
    "object oriented": "Object-Oriented Programming",
}

# ── Load skills list ──────────────────────────────────────────────────────────
_SKILLS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "skills.json"
)

def _load_skills() -> list:
    try:
        with open(_SKILLS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # fallback minimal list if path wrong
        return [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Ruby",
            "React", "Angular", "Vue", "HTML", "CSS", "Node.js", "Next.js",
            "SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
            "Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD", "Git",
            "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
            "Pandas", "NumPy", "Scikit-learn", "Flask", "Django", "FastAPI",
            "REST APIs", "GraphQL", "Microservices", "Linux",
            "Project Management", "Communication", "Excel", "Tableau", "Power BI",
        ]

_SKILLS = _load_skills()
# Pre-build lowercase → canonical map
_SKILL_MAP = {s.lower(): s for s in _SKILLS}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s./+-]", "", text)
    return text


def _match_skill(phrase: str):
    """Returns (canonical_skill, confidence) or None."""
    normalized = _normalize(phrase)

    # 1. Direct map lookup
    if normalized in _SKILL_MAP:
        return (_SKILL_MAP[normalized], "exact")

    # 2. Alias lookup
    if normalized in ALIASES:
        return (ALIASES[normalized], "exact")

    # 3. Fuzzy — skill name appears inside phrase or vice versa
    for skill_lower, skill_canonical in _SKILL_MAP.items():
        if len(skill_lower) >= 3:
            if skill_lower in normalized or normalized in skill_lower:
                return (skill_canonical, "fuzzy")

    return None


# ── Main extraction function ──────────────────────────────────────────────────

def extract_skills(text: str) -> list:
    """
    Extract skills from raw text using keyword + alias matching.
    Returns list of dicts: [{"skill": "React", "confidence": "exact"}, ...]
    """
    found = {}  # skill → confidence

    # Normalize full text
    text_lower = text.lower()

    # Pass 1: direct match for each known skill
    for skill_lower, skill_canonical in _SKILL_MAP.items():
        # Use word boundary matching to avoid partial matches
        pattern = r'(?<![a-z0-9])' + re.escape(skill_lower) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            if skill_canonical not in found:
                found[skill_canonical] = "exact"

    # Pass 2: alias matching
    for alias, canonical in ALIASES.items():
        pattern = r'(?<![a-z0-9])' + re.escape(alias) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            if canonical not in found:
                found[canonical] = "exact"
            elif found[canonical] == "fuzzy":
                found[canonical] = "exact"

    return [{"skill": skill, "confidence": conf} for skill, conf in found.items()]


def extract_skills_list(text: str) -> list:
    """Returns plain list of skill name strings."""
    return [item["skill"] for item in extract_skills(text)]