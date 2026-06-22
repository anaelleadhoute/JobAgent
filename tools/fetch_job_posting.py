import requests
from bs4 import BeautifulSoup

def fetch_job_posting(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n")
    
    # clean up blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)