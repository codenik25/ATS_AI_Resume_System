import pandas as pd
from ml_engine.skill_extractor import load_skills

def load_jobs(csv_path="datasets/job_descriptions.csv"):
    jobs = pd.read_csv(csv_path)
    return jobs


def extract_job_skills(job_description, skills_list):
    job_description = job_description.lower()
    required_skills = []

    for skill in skills_list:
        if skill in job_description:
            required_skills.append(skill)

    return required_skills


def calculate_skill_match(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(job_skills))
    score = (len(matched) / len(job_skills)) * 100
    return round(score, 2)
