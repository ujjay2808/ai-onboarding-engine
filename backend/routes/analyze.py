from flask import Blueprint,request,jsonify
from services.parser import parse_resume,parse_jd
from services.skill_extractor import extract_skills_list as extract_skills
from services.skill_gap import compute_gap
from services.scorer import compute_score
from services.recommender import generate_roadmap

analyze_bp = Blueprint('analyse',__name__)

@analyze_bp.route('/analyze',methods=['POST'])
def analyze():
    resume_file = request.files.get('resume')
    jd_file = request.files.get('jd')

    if not resume_file or not jd_file:
        return jsonify({"error":"Both resume and jd file is required"}), 400
    resume_text = parse_resume(resume_file)
    jd_text = parse_jd(jd_file)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # If JD extraction failed (design-heavy PDF), return helpful error
    if len(jd_skills) == 0:
        return jsonify({"error": "Could not extract skills from JD. Please use a text-based PDF or TXT file."}), 400

    missing_skills = compute_gap(resume_skills, jd_skills)
    match_score = compute_score(resume_skills,jd_skills)
    roadmap = generate_roadmap(missing_skills,resume_skills,jd_skills)

    return jsonify({
        "match_score": match_score,
        "resume_skills" : resume_skills,
        "jd_skills" : jd_skills,
        "missing_skills" : missing_skills,
        "roadmap" : roadmap
    })
