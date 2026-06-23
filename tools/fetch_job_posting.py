import requests
from bs4 import BeautifulSoup

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def fetch_with_requests(url):
    response = requests.get(url, timeout=10, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    response.raise_for_status()
    return clean_text(response.text)

def fetch_with_playwright(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        html = page.content()
        browser.close()
        return clean_text(html)

def fetch_job_posting(url):
    try:
        text = fetch_with_requests(url)
        if len(text) < 500:
            print("→ simple fetch returned too little, trying playwright")
            text = fetch_with_playwright(url)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [403, 401, 429]:
            print(f"→ got {e.response.status_code}, trying playwright")
            text = fetch_with_playwright(url)
        else:
            raise
    except Exception:
        print("→ simple fetch failed, trying playwright")
        text = fetch_with_playwright(url)
    
    return text