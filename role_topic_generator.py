import json

from config import client


def generate_topics(role):

    prompt = f"""
You are an expert technical interviewer.

Generate the most important interview topics for the following role.

Role:
{role}

Rules:

1. Return ONLY valid JSON.
2. No markdown.
3. No explanation.
4. Generate exactly 20 topics.
5. Each topic must contain:

[
    {{
        "role":"{role}",
        "category":"",
        "topic":""
    }}
]

Example:

[
    {{
        "role":"Python Developer",
        "category":"Programming",
        "topic":"Python"
    }},
    {{
        "role":"Python Developer",
        "category":"Programming",
        "topic":"OOP"
    }}
]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text)