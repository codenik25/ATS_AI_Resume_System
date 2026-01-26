import os
import pandas as pd

from ml_engine.preprocess import process_resume
from ml_engine.skill_extractor import load_skills, extract_skills
from ml_engine.job_matcher import load_jobs, extract_job_skills, calculate_skill_match
from ml_engine.semantic_matcher import compute_semantic_similarity
from ml_engine.hybrid_ranker import calculate_final_score
from ml_engine.skill_gap import find_skill_gap


def rank_candidates(resume_folder="datasets/resume_pdfs/"):
    skills_list = load_skills()
    jobs = load_jobs()

    job_title = jobs.iloc[0]["Job_Title"]
    job_desc = jobs.iloc[0]["Job_Description"]
    job_skills = extract_job_skills(job_desc, skills_list)

    results = []

    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            path = os.path.join(resume_folder, file)

            resume_text = process_resume(path)
            resume_skills = extract_skills(resume_text, skills_list)

            skill_score = calculate_skill_match(resume_skills, job_skills)
            semantic_score = compute_semantic_similarity(resume_text, job_desc)
            final_score = calculate_final_score(skill_score, semantic_score)
            missing_skills = find_skill_gap(resume_skills, job_skills)


            results.append({
                           "Candidate": file,
                           "Skill Score": skill_score,
                           "Semantic Score": semantic_score,
                           "Final Score": final_score,
                           "Missing Skills": ", ".join(missing_skills)
                    })


    df = pd.DataFrame(results)
    df = df.sort_values(by="Final Score", ascending=False)

    return job_title, df


if __name__ == "__main__":
    job_title, ranking_df = rank_candidates()

    print(f"\n🎯 Job Role: {job_title}")
    print("\n🏆 Candidate Ranking:\n")
    print(ranking_df)
