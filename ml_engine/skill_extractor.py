from utils.text_cleaner import clean_text

def load_skills(skills_file="datasets/skills.txt"):
    with open(skills_file, "r") as f:
        skills = [skill.strip().lower() for skill in f.readlines() if skill.strip()]
    return skills


def extract_skills(resume_text, skills_list):
    extracted_skills = set()

    resume_text = resume_text.lower()

    for skill in skills_list:
        if skill in resume_text:
            extracted_skills.add(skill)

    return list(extracted_skills)
