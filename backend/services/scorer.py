def compute_score(resume_skills,jd_skills):
    if not jd_skills:
        return  0
    
    resume_lower = [s.lower() for s in resume_skills]
    matched = 0
    
    for skill in jd_skills:
        if skill.lower() in resume_lower:
            matched += 1

    score = round((matched / len(jd_skills)) * 100)
    return score