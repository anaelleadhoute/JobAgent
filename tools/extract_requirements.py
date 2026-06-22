from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_requirements(jd_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a job description parser. Extract structured data from job descriptions and return only valid JSON, nothing else."
            },
            {
                "role": "user",
                "content": f"""Extract the following from this job description and return as JSON:
- company
- role
- must_have_skills (list)
- nice_to_have_skills (list)
- seniority_level

Job description:
{jd_text}"""
            }
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)