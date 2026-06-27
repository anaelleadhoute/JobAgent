from tools.score_fit import score_fit

requirements = {
    "company": "Anthropic",
    "role": "Senior ML Engineer",
    "must_have_skills": ["Python", "PyTorch", "5+ years ML experience"],
    "nice_to_have_skills": ["Kubernetes", "RLHF"],
    "seniority_level": "Senior"
}

result = score_fit(requirements)
print(result)
