from tools.extract_requirements import extract_requirements

jd_text = """
We are looking for a Senior Machine Learning Engineer at Anthropic.
You will work on training and deploying large language models.

Must have:
- Python
- PyTorch
- 5+ years of experience in ML

Nice to have:
- Kubernetes
- experience with RLHF
"""

result = extract_requirements(jd_text)
print(result)