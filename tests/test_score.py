from tools.score_fit import score_fit

requirements = {
    "company": "Anthropic",
    "role": "Senior ML Engineer",
    "must_have_skills": ["Python", "PyTorch", "5+ years ML experience"],
    "nice_to_have_skills": ["Kubernetes", "RLHF"],
    "seniority_level": "Senior"
}

profile = """
- BSc Electrical Engineering, Tel Aviv University
- MSc Computer Science (ML track), Reichman University (ongoing)
- Mobileye (Jan 2023 - Sep 2025): Design Verification Engineer, Python tooling, large-scale simulation data analysis
- Intel (May 2022 - Dec 2022): Logic Design Engineer, RTL/Verilog, Python automation
- Skills: Python, SQL, pandas, NumPy, scikit-learn, OpenAI API, LangGraph, prompt engineering, Git
"""

result = score_fit(requirements, profile)
print(result)