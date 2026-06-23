from tools.fetch_job_posting import fetch_job_posting

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

url = "https://www.glassdoor.com/Job/israel-artificial-intelligence-jobs-SRCH_IL.0,6_IN119_KO7,30.htm"

result = fetch_job_posting(url)
print(result[1000:3500])  # print first 500 chars so it's readable