from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent, reset_conversation

app = FastAPI()

class AnalyzeRequest(BaseModel):
    jd_text: str = None
    url: str = None

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if request.url:
        result = run_agent(f"Analyze this job posting: {request.url}", source_url=request.url)
    elif request.jd_text:
        result = run_agent(request.jd_text)
    else:
        return {"error": "provide either jd_text or url"}
    
    return {"result": result}

@app.post("/reset")
def reset():
    reset_conversation()
    return {"status": "conversation reset"}