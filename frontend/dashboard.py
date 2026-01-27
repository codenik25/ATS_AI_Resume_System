import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from ml_engine.candidate_ranker import rank_candidates
from ml_engine.database import init_db, insert_score, get_leaderboard, get_role_analytics
from ml_engine.suggestions import generate_suggestions

# Initialize database
init_db()

st.set_page_config(page_title="AI Resume Scoring Platform", layout="wide")

st.title("🤖 AI Resume Score Checker & Leaderboard")
st.write("Upload your resume and evaluate your ATS score for different job roles.")

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

# ------------------- RUN ATS SCORING -------------------
if st.button("🔍 Run ATS Score Check") and uploaded_files:

    job_title, ranking_df = rank_candidates()

    st.subheader(f"🎯 Job Role: {job_title}")
    st.dataframe(ranking_df)

    st.subheader("📊 Candidate Scores Visualization")
    st.bar_chart(ranking_df.set_index("Candidate")["Final Score"])

    # Download CSV
    csv = ranking_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Ranking Report", csv, "candidate_ranking.csv", "text/csv")

    # ------------------- USER RESULT -------------------
    user_file = uploaded_files[0].name
    user_row = ranking_df[ranking_df["Candidate"] == user_file]

    if name and not user_row.empty:
        skill_score = float(user_row["Skill Score"].values[0])
        semantic_score = float(user_row["Semantic Score"].values[0])
        final_score = float(user_row["Final Score"].values[0])

        insert_score(name, job_role, skill_score, semantic_score, final_score)
        st.success("✅ Your score saved to leaderboard!")

        # Score breakdown
        st.subheader("📊 Your Score Breakdown")
        breakdown = pd.DataFrame({
            "Metric": ["Skill Match", "Semantic Match"],
            "Score": [skill_score, semantic_score]
        })
        st.bar_chart(breakdown.set_index("Metric"))

        # Suggestions
        st.subheader("🧠 Resume Improvement Suggestions")
        if "Missing Skills" in ranking_df.columns:
            missing_skills = user_row["Missing Skills"].values[0]
            st.info(generate_suggestions(missing_skills, job_role))

# ------------------- LEADERBOARD -------------------
st.subheader("🏆 Leaderboard")

rows = get_leaderboard(job_role)
if rows:
    df = pd.DataFrame(rows, columns=["Name", "Final Score"])
    st.dataframe(df)

    if name and name in df["Name"].values[:10]:
        st.success("🎖 You are in Top 10 for this role!")

# ------------------- ROLE ANALYTICS -------------------
st.subheader("📈 Role-wise Analytics")

analytics_rows = get_role_analytics()
if analytics_rows:
    analytics_df = pd.DataFrame(
        analytics_rows,
        columns=["Job Role", "Total Candidates", "Average Score"]
    )
    st.dataframe(analytics_df)
    st.bar_chart(analytics_df.set_index("Job Role")["Average Score"])

# ------------------- RESUME COMPARISON -------------------
st.subheader("🆚 Resume Comparison")

if rows and len(rows) >= 2:
    df_compare = pd.DataFrame(rows, columns=["Name", "Final Score"])

    candidate1 = st.selectbox("Select Candidate 1", df_compare["Name"])
    candidate2 = st.selectbox("Select Candidate 2", df_compare["Name"], index=1)

    if st.button("Compare Candidates"):
        score1 = df_compare[df_compare["Name"] == candidate1]["Final Score"].values[0]
        score2 = df_compare[df_compare["Name"] == candidate2]["Final Score"].values[0]

        compare_df = pd.DataFrame({
            "Candidate": [candidate1, candidate2],
            "Score": [score1, score2]
        })

        st.bar_chart(compare_df.set_index("Candidate"))
