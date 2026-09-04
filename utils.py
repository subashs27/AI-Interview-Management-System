import re

def clean_json_response(response_text):
    text = response_text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = re.sub(r',\s*([\]}])', r'\1', text)

    return text