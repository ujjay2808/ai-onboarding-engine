"""
skill_extractor.py — Enhanced skill extraction using keyword matching + alias normalization.
"""

import json
import os
import re

ALIASES = {
    "js": "JavaScript", "javascript": "JavaScript", "ts": "TypeScript",
    "typescript": "TypeScript", "py": "Python", "ml": "Machine Learning",
    "dl": "Deep Learning", "nlp": "NLP", "ai": "Artificial Intelligence",
    "cv": "Computer Vision", "sql": "SQL", "nosql": "MongoDB",
    "node": "Node.js", "nodejs": "Node.js", "node.js": "Node.js",
    "react": "React", "reactjs": "React", "vue": "Vue", "vuejs": "Vue",
    "angular": "Angular", "angularjs": "Angular", "k8s": "Kubernetes",
    "aws": "AWS", "gcp": "GCP", "azure": "Azure", "tf": "TensorFlow",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "pg": "PostgreSQL",
    "postgres": "PostgreSQL", "mongo": "MongoDB", "mongodb": "MongoDB",
    "git": "Git", "ci/cd": "CI/CD", "cicd": "CI/CD",
    "oop": "Object-Oriented Programming", "html": "HTML", "css": "CSS",
    "scss": "CSS", "rest": "REST APIs", "restful": "REST APIs",
    "graphql": "GraphQL", "excel": "Excel", "tableau": "Tableau",
    "powerbi": "Power BI", "power bi": "Power BI",
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "natural language processing": "NLP", "computer vision": "Computer Vision",
    "data structures": "Data Structures",
    "object oriented": "Object-Oriented Programming",
}

_SKILLS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "skills.json")
if not os.path.exists(_SKILLS_PATH):
    _SKILLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skills.json")

def _load_skills():
    try:
        with open(_SKILLS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "Go",
            "React", "Angular", "Vue", "HTML", "CSS", "Node.js",
            "SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
            "Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD", "Git",
            "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
            "Flask", "Django", "REST APIs", "GraphQL", "Linux",
            "Excel", "Tableau", "Power BI",
        ]

_SKILLS = _load_skills()
_SKILL_MAP = {s.lower(): s for s in _SKILLS}

def extract_skills(text):
    found = {}
    text_lower = text.lower()

    for skill_lower, skill_canonical in _SKILL_MAP.items():
        pattern = r'(?<![a-z0-9])' + re.escape(skill_lower) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            if skill_canonical not in found:
                found[skill_canonical] = "exact"

    for alias, canonical in ALIASES.items():
        pattern = r'(?<![a-z0-9])' + re.escape(alias) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            if canonical not in found:
                found[canonical] = "exact"

    return [{"skill": skill, "confidence": conf} for skill, conf in found.items()]

def extract_skills_list(text):
    return [item["skill"] for item in extract_skills(text)]