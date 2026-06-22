from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_fit(requirements, profile):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""You are an honest career advisor. Compare these job requirements against this candidate profile and return a fit score.

Be honest and direct — if the fit is weak, say so explicitly. Never flatter or soften a weak fit.

Return only valid JSON with these fields:
- fit_score (integer 0-100)
- missing_skills (list of skills the candidate lacks)
- summary (2-3 sentences, honest assessment)

Job requirements:
{json.dumps(requirements, indent=2)}

Candidate profile:
{profile}"""
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)