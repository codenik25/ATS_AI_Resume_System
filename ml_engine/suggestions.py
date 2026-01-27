def generate_suggestions(missing_skills):
    if not missing_skills:
        return "🎉 Excellent! Your resume matches most of the required skills."

    tips = "📌 To improve your ATS score, consider adding these skills:\n"
    for skill in missing_skills:
        tips += f"• {skill}\n"

    tips += "\n💡 Try adding these skills in your projects, experience, or skills section."
    return tips
