from tools.log_analysis import log_analysis

result = log_analysis(
    company="Test Company",
    role="Test Role",
    fit_score=75,
    missing_skills="Docker, Kubernetes",
    source_url=None
)

print(result)