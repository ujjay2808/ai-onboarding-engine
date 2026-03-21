import json
import os
from collections import deque

# Skill dependency graph — prerequisites first
SKILL_GRAPH = {
    'React': ['JavaScript', 'HTML', 'CSS'],
    'Node.js': ['JavaScript'],
    'Next.js': ['React', 'JavaScript'],
    'Express': ['JavaScript', 'Node.js'],
    'Angular': ['JavaScript', 'TypeScript'],
    'Vue': ['JavaScript', 'HTML'],
    'TypeScript': ['JavaScript'],
    'TensorFlow': ['Python', 'Machine Learning'],
    'PyTorch': ['Python', 'Machine Learning'],
    'Deep Learning': ['Machine Learning', 'Python'],
    'Machine Learning': ['Python'],
    'Natural Language Processing': ['Python', 'Machine Learning'],
    'Pandas': ['Python'],
    'NumPy': ['Python'],
    'Kubernetes': ['Docker'],
    'PostgreSQL': ['SQL'],
    'MongoDB': ['SQL'],
}

# Load courses
courses_path = os.path.join(os.path.dirname(__file__), '../../data/courses.json')
with open(courses_path, 'r') as f:
    COURSES = json.load(f)

def generate_roadmap(missing_skills, resume_skills, jd_skills):
    resume_lower = [s.lower() for s in resume_skills]
    ordered = bfs_order(missing_skills, resume_lower)
    
    roadmap = []
    week = 1

    for skill in ordered:
        prerequisites = SKILL_GRAPH.get(skill, [])
        missing_prereqs = [p for p in prerequisites 
                          if p.lower() not in resume_lower]
        
        reason = generate_reason(skill, missing_prereqs, week)
        resources = COURSES.get(skill, [])
        difficulty = get_difficulty(skill)

        roadmap.append({
            "skill": skill,
            "week": week,
            "difficulty": difficulty,
            "reason": reason,
            "resources": resources
        })
        week += 1

    return roadmap

def bfs_order(missing_skills, resume_lower):
    ordered = []
    visited = set()
    queue = deque(missing_skills)

    while queue:
        skill = queue.popleft()
        if skill in visited:
            continue
        
        prerequisites = SKILL_GRAPH.get(skill, [])
        missing_prereqs = [p for p in prerequisites 
                          if p.lower() not in resume_lower 
                          and p not in visited]
        
        if missing_prereqs:
            for prereq in missing_prereqs:
                if prereq not in visited:
                    queue.appendleft(skill)
                    queue.appendleft(prereq)
                    break
        else:
            visited.add(skill)
            ordered.append(skill)

    return ordered

def generate_reason(skill, missing_prereqs, week):
    reason = f"{skill} recommended because: "
    reason += "(1) Required in job description. "
    reason += "(2) Not found in your resume. "
    
    if missing_prereqs:
        prereq_str = ', '.join(missing_prereqs)
        reason += f"(3) Prerequisites {prereq_str} scheduled before this. "
    else:
        reason += "(3) No prerequisites needed. "
    
    reason += "Confidence: High."
    return reason

def get_difficulty(skill):
    beginner = ['HTML', 'CSS', 'Git', 'Excel', 'SQL', 'Python']
    advanced = ['Kubernetes', 'Deep Learning', 'TensorFlow', 
                'PyTorch', 'Natural Language Processing']
    
    if skill in beginner:
        return "Beginner"
    elif skill in advanced:
        return "Advanced"
    else:
        return "Intermediate"