from openai import OpenAI
import json
import os

from tools.fetch_job_posting import fetch_job_posting
from tools.extract_requirements import extract_requirements
from tools.score_fit import score_fit
from tools.log_analysis import log_analysis
from tools.query_analyses import query_analyses

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a personal job fit advisor for Anaelle, an MSc Computer Science student with a background in Electrical Engineering and experience at Mobileye and Intel. Given a job description, you:
1. Extract requirements using extract_requirements
2. Score fit using score_fit — be honest, no flattery
3. Log the analysis using log_analysis
4. Return a warm, direct, personal summary addressed to Anaelle: her fit score, what she's missing, and an honest assessment of whether she should apply."""

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
            "description": "Scores fit between job requirements and candidate profile. Retrieves relevant profile entries automatically via RAG. Must be honest, no flattery.",
            "parameters": {
                "type": "object",
                "properties": {
                    "requirements": {"type": "object", "description": "Extracted job requirements"}
                },
                "required": ["requirements"]
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

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def reset_conversation():
    global conversation_history
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def run_agent(user_input, source_url=None):
    conversation_history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            conversation_history.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"→ calling {name} with {args}")

                if name == "fetch_job_posting":
                    result = fetch_job_posting(**args)
                elif name == "extract_requirements":
                    result = extract_requirements(**args)
                elif name == "score_fit":
                    result = score_fit(**args)
                elif name == "log_analysis":
                    if source_url:
                        args["source_url"] = source_url
                    result = log_analysis(**args)
                elif name == "query_analyses":
                    result = query_analyses(**args)
                else:
                    result = {"error": "unknown tool"}

                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        else:
            conversation_history.append({"role": "assistant", "content": message.content})
            return message.content
