import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent import run_agent


jd_text = """
We are looking for a Senior Machine Learning Engineer at Anthropic.
You will work on training and deploying large language models.

Must have:
- Python
- PyTorch
- 5+ years of experience in ML

Nice to have:
- Kubernetes
- RLHF experience
"""

result = run_agent(jd_text)
print(result)