from ml_engine.preprocess import process_resume
from ml_engine.job_matcher import load_jobs
from ml_engine.semantic_matcher import compute_semantic_similarity

resume_text = process_resume("datasets/resume_pdfs/sample_resume.pdf")

jobs = load_jobs()

job_title = jobs.iloc[0]["Job_Title"]
job_desc = jobs.iloc[0]["Job_Description"]

score = compute_semantic_similarity(resume_text, job_desc)

print("\nJob Title:", job_title)
print("🤖 AI Semantic Match Score:", score, "%")
