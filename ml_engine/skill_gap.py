def find_skill_gap(resume_skills, job_skills):
    missing_skills = set(job_skills) - set(resume_skills)
    return list(missing_skills)
