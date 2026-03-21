def compute_gap(resume_skills,jd_skills):
    resume_lower = [s.lower() for s in resume_skills]
    missing = []

    for skill in jd_skills:
        if skill.lower() not in resume_lower:
            missing.append(skill)
    return missing