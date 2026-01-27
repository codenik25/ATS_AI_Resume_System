from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_semantic_similarity(resume_text, job_description):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    similarity_score = util.cos_sim(resume_embedding, job_embedding)

    # Convert to percentage
    score = float(similarity_score[0][0]) * 100
    return round(score, 2)
