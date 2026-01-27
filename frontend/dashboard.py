import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from ml_engine.candidate_ranker import rank_candidates
from ml_engine.database import init_db, insert_score, get_leaderboard

# Initialize database
init_db()

st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("🤖 AI Resume Score Checker & Leaderboard")
st.write("Upload your resume and see how well it matches your dream job!")

# ------------------- USER INFO -------------------
st.subheader("👤 Candidate Info")

name = st.text_input("Enter Your Name")
job_role = st.selectbox(
    "Select Job Role",
    ["Data Scientist", "Backend Developer", "ML Engineer"]
)

# ------------------- RESUME UPLOAD -------------------
uploaded_files = st.file_uploader(
    "📤 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("datasets/resume_pdfs", exist_ok=True)
    for file in uploaded_files:
        save_path = f"datasets/resume_pdfs/{file.name}"
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
    st.success("Resumes uploaded successfully!")

# ------------------- RUN RANKING -------------------
if st.button("🔍 Run ATS Score Check"):

    job_title, ranking_df = rank_candidates()

    st.subheader(f"🎯 Job Role: {job_title}")
    st.dataframe(ranking_df)

    # Score Visualization
    st.subheader("📊 Candidate Scores Visualization")
    st.bar_chart(ranking_df.set_index("Candidate")["Final Score"])

    # Download Report
    csv = ranking_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Ranking Report",
        data=csv,
        file_name='candidate_ranking.csv',
        mime='text/csv',
    )

    # ------------------- SAVE USER SCORE -------------------
    if name:
        user_row = ranking_df[ranking_df["Candidate"] == uploaded_files[0].name]

        if not user_row.empty:
            skill_score = float(user_row["Skill Score"].values[0])
            semantic_score = float(user_row["Semantic Score"].values[0])
            final_score = float(user_row["Final Score"].values[0])

            insert_score(name, job_role, skill_score, semantic_score, final_score)
            st.success("✅ Your score has been saved to the leaderboard!")

            # Score Breakdown Graph
            st.subheader("📊 Your Score Breakdown")
            breakdown = pd.DataFrame({
                "Metric": ["Skill Match", "Semantic Match"],
                "Score": [skill_score, semantic_score]
            })
            st.bar_chart(breakdown.set_index("Metric"))

    # ------------------- LEADERBOARD -------------------
    st.subheader("🏆 Leaderboard")

    rows = get_leaderboard(job_role)

    if rows:
        df = pd.DataFrame(rows, columns=["Name", "Final Score"])
        st.dataframe(df)

        if name and name in df["Name"].values[:10]:
            st.success("🎖 You are in Top 10 for this role!")
