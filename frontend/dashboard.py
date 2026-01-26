import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from ml_engine.candidate_ranker import rank_candidates

st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("🤖 AI-Powered Resume Screening Dashboard")
st.write("This system ranks candidates based on Skill Match + Semantic AI Match.")

# Resume upload
uploaded_files = st.file_uploader(
    "📤 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        save_path = f"datasets/resume_pdfs/{file.name}"
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
    st.success("Resumes uploaded successfully!")

# Button to run ranking
if st.button("🔍 Run Candidate Ranking"):
    job_title, ranking_df = rank_candidates()

    st.subheader(f"🎯 Job Role: {job_title}")
    st.dataframe(ranking_df)

    # Chart
    st.subheader("📊 Candidate Scores Visualization")
    st.bar_chart(ranking_df.set_index("Candidate")["Final Score"])

    # ✅ DOWNLOAD BUTTON MUST BE HERE
    csv = ranking_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Ranking Report",
        data=csv,
        file_name='candidate_ranking.csv',
        mime='text/csv',
    )
