"""
skill_extractor.py — Rutvi's Task R1
Enhanced skill extraction using spaCy NER + keyword matching + alias normalization.
Backward compatible: extract_skills(text) still works as before.
"""

import json
import os
import re
import spacy

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
    "pytorch": "PyTorch",
    "pg": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "git": "Git",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "oop": "Object-Oriented Programming",
    "ds": "Data Structures",
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
}

# Load spaCy model once at module level
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model not found. Run: python -m spacy download en_core_web_sm"
    )

# ── Load skills list ──────────────────────────────────────────────────────────
_SKILLS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "skills.json"
)

def _load_skills() -> list[str]:
    with open(_SKILLS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_SKILLS: list[str] = _load_skills()
# Pre-build a lowercase → canonical map for O(1) lookup
_SKILL_MAP: dict[str, str] = {s.lower(): s for s in _SKILLS}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Lowercase, strip punctuation (except / and . for things like CI/CD, Node.js)."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s./+-]", "", text)
    return text


def _resolve_alias(token: str) -> str | None:
    """Return canonical skill name if token matches an alias, else None."""
    return ALIASES.get(_normalize(token))


def _match_skill(phrase: str) -> tuple[str, str] | None:
    """
    Try to match a phrase to a known skill.
    Returns (canonical_skill, confidence) or None.
    confidence is 'exact' or 'fuzzy'.
    """
    normalized = _normalize(phrase)

    # 1. Direct map lookup (exact)
    if normalized in _SKILL_MAP:
        return (_SKILL_MAP[normalized], "exact")

    # 2. Alias lookup (exact)
    alias_result = _resolve_alias(normalized)
    if alias_result:
        return (alias_result, "exact")

    # 3. Substring fuzzy match — skill name appears inside the phrase
    for skill_lower, skill_canonical in _SKILL_MAP.items():
        if skill_lower in normalized or normalized in skill_lower:
            return (skill_canonical, "fuzzy")

    return None


# ── Main extraction function ──────────────────────────────────────────────────

def extract_skills(text: str) -> list[dict]:
    """
    Extract skills from raw text using spaCy + keyword matching.

    Returns a list of dicts:
        [{"skill": "React", "confidence": "exact"}, ...]

    Backward-compatible wrapper `extract_skills_list(text)` returns plain list of strings.
    """
    doc = nlp(text)
    found: dict[str, str] = {}  # skill → confidence (keep highest)

    # ── Pass 1: Check individual tokens (lemmatized) ──────────────────────────
    for token in doc:
        if token.is_stop or token.is_punct or len(token.text) < 2:
            continue
        # Try original surface form
        match = _match_skill(token.text)
        if match:
            skill, conf = match
            # prefer 'exact' over 'fuzzy'
            if skill not in found or conf == "exact":
                found[skill] = conf
            continue
        # Try lemma
        match = _match_skill(token.lemma_)
        if match:
            skill, conf = match
            if skill not in found or conf == "exact":
                found[skill] = conf

    # ── Pass 2: noun_chunks — catches multi-word skills like "machine learning" ─
    for chunk in doc.noun_chunks:
        match = _match_skill(chunk.text)
        if match:
            skill, conf = match
            if skill not in found or conf == "exact":
                found[skill] = conf

    # ── Pass 3: sliding n-grams (up to 4 words) for edge cases ──────────────
    words = [t.text for t in doc if not t.is_punct]
    for n in range(2, 5):
        for i in range(len(words) - n + 1):
            phrase = " ".join(words[i : i + n])
            match = _match_skill(phrase)
            if match:
                skill, conf = match
                if skill not in found or conf == "exact":
                    found[skill] = conf

    return [{"skill": skill, "confidence": conf} for skill, conf in found.items()]


def extract_skills_list(text: str) -> list[str]:
    """Backward-compatible wrapper — returns plain list of skill name strings."""
    return [item["skill"] for item in extract_skills(text)]
