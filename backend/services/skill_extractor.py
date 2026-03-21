import json
import os
import re

# Load skills list
skills_path = os.path.join(os.path.dirname(__file__), '../../data/skills.json')
with open(skills_path, 'r') as f:
    SKILLS_LIST = json.load(f)

# Common aliases
ALIASES = {
    'js': 'JavaScript',
    'ml': 'Machine Learning',
    'dl': 'Deep Learning',
    'nlp': 'Natural Language Processing',
    'ts': 'TypeScript',
    'k8s': 'Kubernetes',
    'tf': 'TensorFlow'
}

def clean_text(text):
    # Remove extra spaces and hyphens that PDFs add
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\w)\s*-\s*(\w)', r'\1\2', text)
    return text.lower()

def extract_skills(text):
    cleaned = clean_text(text)
    found_skills = []

    # Check aliases first
    words = cleaned.split()
    for alias, skill in ALIASES.items():
        if alias in words:
            if skill not in found_skills:
                found_skills.append(skill)

    # Check against skills list
    for skill in SKILLS_LIST:
        if skill.lower() in cleaned:
            if skill not in found_skills:
                found_skills.append(skill)

    return found_skills