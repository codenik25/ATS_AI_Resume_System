def calculate_final_score(skill_score, semantic_score, skill_weight=0.4, semantic_weight=0.6):
    final_score = (skill_score * skill_weight) + (semantic_score * semantic_weight)
    return round(final_score, 2)
