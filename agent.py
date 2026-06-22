from openai import OpenAI
import json
import os

from tools.fetch_job_posting import fetch_job_posting
from tools.extract_requirements import extract_requirements
from tools.score_fit import score_fit
from tools.log_analysis import log_analysis
from tools.query_analyses import query_analyses

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_job_posting",
            "description": "Fetches raw text from a job posting URL. Use only if a URL is provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The job posting URL"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_requirements",
            "description": "Extracts structured requirements from raw job description text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "jd_text": {"type": "string", "description": "Raw job description text"}
                },
                "required": ["jd_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "score_fit",
            "description": "Scores fit between job requirements and candidate profile. Must be honest, no flattery.",
            "parameters": {
                "type": "object",
                "properties": {
                    "requirements": {"type": "object", "description": "Extracted job requirements"},
                    "profile": {"type": "string", "description": "Candidate profile text"}
                },
                "required": ["requirements", "profile"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_analysis",
            "description": "Logs the analysis to the database. Always call this after scoring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "role": {"type": "string"},
                    "fit_score": {"type": "integer"},
                    "missing_skills": {"type": "string"},
                    "source_url": {"type": "string"}
                },
                "required": ["company", "role", "fit_score", "missing_skills"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_analyses",
            "description": "Queries past analyses from the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_sql": {"type": "string", "description": "Optional SQL WHERE clause"}
                },
                "required": []
            }
        }
    }
]

PROFILE = """
- BSc Electrical Engineering, Tel Aviv University
- MSc Computer Science (ML track), Reichman University (ongoing)
- Mobileye (Jan 2023 - Sep 2025): Design Verification Engineer, Python tooling, large-scale simulation data analysis
- Intel (May 2022 - Dec 2022): Logic Design Engineer, RTL/Verilog, Python automation
- Skills: Python, SQL, pandas, NumPy, scikit-learn, OpenAI API, LangGraph, prompt engineering, Git
"""

def run_agent(user_input, source_url=None):
    messages = [
        {
            "role": "system",
            "content": """You are a job fit analyzer. Given a job description, you:
1. Extract requirements using extract_requirements
2. Score fit using score_fit — be honest, no flattery
3. Log the analysis using log_analysis
4. Return a clear summary: score, missing skills, honest assessment"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"→ calling {name} with {args}")

                if name == "fetch_job_posting":
                    result = fetch_job_posting(**args)
                elif name == "extract_requirements":
                    result = extract_requirements(**args)
                elif name == "score_fit":
                    args["profile"] = PROFILE
                    result = score_fit(**args)
                elif name == "log_analysis":
                    if source_url:
                        args["source_url"] = source_url
                    result = log_analysis(**args)
                elif name == "query_analyses":
                    result = query_analyses(**args)
                else:
                    result = {"error": "unknown tool"}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        else:
            return message.content