"""
reasoning_trace.py — Rutvi's Task R2
Generates human-readable reasoning for each skill recommendation.
"""


def generate_trace(
    skill: str,
    resume_skills: list[str],
    jd_skills: list[str],
    prerequisites: list[str],
    week_number: int,
    confidence: str = "High",
) -> str:
    """
    Build a reasoning trace string for a recommended skill.

    Args:
        skill:          The skill being recommended (e.g. "React")
        resume_skills:  Skills found in the candidate's resume
        jd_skills:      Skills found in the job description
        prerequisites:  Prerequisites for this skill (from dependency graph)
        week_number:    Which week in the roadmap this skill is scheduled
        confidence:     Confidence level from skill extractor ("exact" → "High", else "Medium")

    Returns:
        A single human-readable string explaining the recommendation.
    """
    reasons = []
    counter = 1

    # ── Reason 1: In JD ───────────────────────────────────────────────────────
    if skill in jd_skills:
        reasons.append(f"({counter}) Listed as required in the job description.")
        counter += 1
    else:
        reasons.append(f"({counter}) Highly relevant to the role even if not explicitly listed.")
        counter += 1

    # ── Reason 2: Missing from resume ────────────────────────────────────────
    if skill not in resume_skills:
        reasons.append(f"({counter}) Not found in your resume — this is a gap to fill.")
        counter += 1
    else:
        reasons.append(f"({counter}) Present in your resume but needs strengthening.")
        counter += 1

    # ── Reason 3: Prerequisite ordering ──────────────────────────────────────
    if prerequisites:
        # Separate prereqs already in resume vs also missing
        covered = [p for p in prerequisites if p in resume_skills]
        also_missing = [p for p in prerequisites if p not in resume_skills]

        if also_missing and week_number > 1:
            prereq_str = ", ".join(also_missing)
            reasons.append(
                f"({counter}) Scheduled Week {week_number} because prerequisite(s) "
                f"{prereq_str} are being covered in earlier weeks first."
            )
        elif covered:
            prereq_str = ", ".join(covered)
            reasons.append(
                f"({counter}) Scheduled Week {week_number} — prerequisite(s) "
                f"{prereq_str} already present in your resume, so you can start sooner."
            )
        else:
            reasons.append(
                f"({counter}) Scheduled Week {week_number} based on dependency ordering."
            )
        counter += 1
    else:
        reasons.append(
            f"({counter}) No prerequisites required — good starting point, scheduled Week {week_number}."
        )
        counter += 1

    # ── Confidence label ──────────────────────────────────────────────────────
    confidence_label = "High" if confidence in ("exact", "High") else "Medium"
    confidence_note = f"Confidence: {confidence_label}."

    trace = (
        f"{skill} recommended because: "
        + " ".join(reasons)
        + " "
        + confidence_note
    )
    return trace


# ── Batch helper ──────────────────────────────────────────────────────────────

def add_traces_to_roadmap(
    roadmap: list[dict],
    resume_skills: list[str],
    jd_skills: list[str],
) -> list[dict]:
    """
    Iterate over a roadmap list and attach a 'reason' string to each item.

    Each roadmap item is expected to have:
        skill, week, prerequisites_needed (list), confidence (optional)

    Returns the same list with 'reason' populated.
    """
    for item in roadmap:
        item["reason"] = generate_trace(
            skill=item["skill"],
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            prerequisites=item.get("prerequisites_needed", []),
            week_number=item.get("week", 1),
            confidence=item.get("confidence", "High"),
        )
    return roadmap
