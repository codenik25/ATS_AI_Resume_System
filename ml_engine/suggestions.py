def generate_suggestions(missing_skills, job_role):
    if not missing_skills:
        return f"🎉 Excellent! Your resume is highly optimized for the {job_role} role."

    suggestions = f"🛠 To improve your ATS score for {job_role}, consider adding:\n\n"

    for skill in missing_skills:
        suggestions += f"• {skill}\n"

    suggestions += "\n📌 Tip: Add these skills in Projects, Experience, or Skills section."

    return suggestions
