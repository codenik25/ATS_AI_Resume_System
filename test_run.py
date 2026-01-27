import pandas as pd

# Load resume dataset
resumes = pd.read_csv("datasets/resumes.csv")
print("Resumes loaded:", resumes.shape)

# Load job descriptions
jobs = pd.read_csv("datasets/job_descriptions.csv")
print("Jobs loaded:", jobs.shape)

# Load skills
with open("datasets/skills.txt") as f:
    skills = f.read().splitlines()

print("Skills loaded:", len(skills))
print("Sample skills:", skills[:5])
