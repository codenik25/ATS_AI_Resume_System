from ml_engine.preprocess import process_resume
from ml_engine.skill_extractor import load_skills, extract_skills
from ml_engine.job_matcher import load_jobs, extract_job_skills, calculate_skill_match
from ml_engine.semantic_matcher import compute_semantic_similarity
from ml_engine.hybrid_ranker import calculate_final_score

resume_text = process_resume("datasets/resume_pdfs/sample_resume.pdf")

skills_list = load_skills()
resume_skills = extract_skills(resume_text, skills_list)

jobs = load_jobs()
job_title = jobs.iloc[0]["Job_Title"]
job_desc = jobs.iloc[0]["Job_Description"]

job_skills = extract_job_skills(job_desc, skills_list)
skill_score = calculate_skill_match(resume_skills, job_skills)

semantic_score = compute_semantic_similarity(resume_text, job_desc)

final_score = calculate_final_score(skill_score, semantic_score)

print("\n📌 Job Title:", job_title)
print("Skill Score:", skill_score, "%")
print("Semantic Score:", semantic_score, "%")
print("🚀 FINAL HYBRID SCORE:", final_score, "%")
