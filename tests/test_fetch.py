from tools.fetch_job_posting import fetch_job_posting

url = "https://www.linkedin.com/jobs/view/4426494172/"

result = fetch_job_posting(url)
print(result[1000:3500])  # print first 500 chars so it's readable