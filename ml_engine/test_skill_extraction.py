import os
from ml_engine.preprocess import process_resume
from ml_engine.skill_extractor import load_skills, extract_skills

sample_pdf = "datasets/resume_pdfs/sample_resume.pdf"

if not os.path.exists(sample_pdf):
    print("❌ Resume PDF not found")
else:
    resume_text = process_resume(sample_pdf)
    skills_list = load_skills()
    extracted_skills = extract_skills(resume_text, skills_list)

    print("\n===== EXTRACTED SKILLS =====")
    print(extracted_skills)
