"""Compare catalog mentions, not suitability or required/optional job criteria."""
from app.services.skill_extractor import extract_skills
from app.services.job_requirements import classify_job_requirements


def compare_job_description(resume_text: str | None, job_description: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    text_available = bool(resume_text and resume_text.strip())
    matched = resume_skills & job_skills
    classified = {row['skill']: row for row in classify_job_requirements(job_description)}
    # Whole-text extraction can join aliases across lines ("Java\nScript").
    # Preserve the scoring catalog and abstain when fragment evidence is absent.
    requirements = [classified.get(skill, {
        'skill': skill, 'category': 'uncertain',
        'evidence': [{'text': job_description.strip(), 'category': 'uncertain'}],
    }) for skill in sorted(job_skills, key=str.casefold)]
    return {
        'requirements': requirements,
        'text_available': text_available,
        'job_skills': sorted(job_skills, key=str.casefold),
        'matched_skills': sorted(matched, key=str.casefold),
        'not_detected_skills': sorted(job_skills - resume_skills, key=str.casefold),
        'skill_overlap_percent': round(100 * len(matched) / len(job_skills), 1)
        if text_available and job_skills else None,
    }
