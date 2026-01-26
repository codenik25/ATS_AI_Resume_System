from ml_engine.preprocess import process_resume
from ml_engine.skill_extractor import load_skills, extract_skills
from ml_engine.job_matcher import load_jobs, extract_job_skills, calculate_skill_match

# Load resume
resume_text = process_resume("datasets/resume_pdfs/sample_resume.pdf")
skills_list = load_skills()
resume_skills = extract_skills(resume_text, skills_list)

print("Resume Skills:", resume_skills)

# Load job descriptions
jobs = load_jobs()

# Test with first job
job_title = jobs.iloc[0]["Job_Title"]
job_desc = jobs.iloc[0]["Job_Description"]

job_skills = extract_job_skills(job_desc, skills_list)

print("\nJob Title:", job_title)
print("Required Skills:", job_skills)

# Calculate match score
score = calculate_skill_match(resume_skills, job_skills)

print("\n🎯 SKILL MATCH SCORE:", score, "%")
