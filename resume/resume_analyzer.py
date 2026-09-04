"""
Resume Analyzer

Extracts structured candidate information from a resume
using Gemini with JSON response enforcement.
"""

import json
import re
import streamlit as st

from google.genai import types

from config import client
from resume_prompt import RESUME_PROMPT


REQUIRED_KEYS = [
    "name",
    "target_role",
    "skills",
    "experience",
    "projects",
    "certifications"
]


def clean_resume_json(text):
    """
    Clean common formatting problems from Gemini output.
    """

    if not text:
        raise ValueError("Gemini returned an empty response.")

    text = text.strip()

    # Remove markdown code fences
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # Remove trailing commas
    text = re.sub(
        r",\s*([}\]])",
        r"\1",
        text
    )

    return text


def repair_json_strings(text):
    """
    Repair unescaped control characters inside JSON strings.

    This handles cases where Gemini accidentally places
    a raw newline/tab inside a quoted string.
    """

    result = []

    inside_string = False
    escaped = False

    for char in text:

        if char == '"' and not escaped:

            inside_string = not inside_string

            result.append(char)

            continue

        if inside_string:

            if char == "\n":
                result.append("\\n")
                continue

            if char == "\r":
                result.append("\\r")
                continue

            if char == "\t":
                result.append("\\t")
                continue

        result.append(char)

        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False

    return "".join(result)


def analyze_resume(resume_text):

    print("=" * 80)
    print("🤖 ANALYZING RESUME")
    print("=" * 80)

    if not resume_text or not resume_text.strip():

        raise ValueError(
            "Resume text is empty."
        )

    print("Resume Length:", len(resume_text))

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = (
        RESUME_PROMPT
        + "\n\n"
        + resume_text
    )

    # --------------------------------------------------
    # Gemini
    # --------------------------------------------------

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                temperature=0

            )
        )

    except Exception as e:

        st.error(
            f"Gemini Error: {e}"
        )

        raise

    raw_response = response.text

    print("=" * 80)
    print("RAW GEMINI RESPONSE")
    print("=" * 80)
    print(raw_response)
    print("=" * 80)

    # --------------------------------------------------
    # Clean
    # --------------------------------------------------

    cleaned = clean_resume_json(
        raw_response
    )

    # --------------------------------------------------
    # First JSON parse
    # --------------------------------------------------

    try:

        candidate = json.loads(
            cleaned
        )

    except json.JSONDecodeError:

        print("=" * 80)
        print("⚠️ FIRST JSON PARSE FAILED")
        print("=" * 80)

        # Try repairing newlines/tabs inside strings
        repaired = repair_json_strings(
            cleaned
        )

        # Remove trailing commas again
        repaired = re.sub(
            r",\s*([}\]])",
            r"\1",
            repaired
        )

        try:

            candidate = json.loads(
                repaired
            )

            print(
                "✅ JSON repaired successfully"
            )

        except json.JSONDecodeError as e:

            print("=" * 80)
            print("❌ FINAL JSON PARSE FAILED")
            print("=" * 80)
            print(repaired)
            print("=" * 80)

            raise ValueError(
                "Gemini returned malformed resume JSON. "
                "Check the raw response printed in the terminal."
            ) from e

    # --------------------------------------------------
    # Validate object
    # --------------------------------------------------

    if not isinstance(candidate, dict):

        raise ValueError(
            "Gemini response is not a JSON object."
        )

    # --------------------------------------------------
    # Required fields
    # --------------------------------------------------

    missing_keys = [

        key

        for key in REQUIRED_KEYS

        if key not in candidate

    ]

    if missing_keys:

        raise ValueError(
            f"Missing fields from resume analysis: "
            f"{missing_keys}"
        )

    # --------------------------------------------------
    # Normalize fields
    # --------------------------------------------------

    candidate["name"] = str(
        candidate.get("name", "")
    ).strip()

    candidate["target_role"] = str(
        candidate.get("target_role", "")
    ).strip()

    if not isinstance(
        candidate["skills"],
        list
    ):
        candidate["skills"] = []

    if not isinstance(
        candidate["experience"],
        list
    ):
        candidate["experience"] = []

    if not isinstance(
        candidate["projects"],
        list
    ):
        candidate["projects"] = []

    if not isinstance(
        candidate["certifications"],
        list
    ):
        candidate["certifications"] = []

    # --------------------------------------------------
    # Basic validation
    # --------------------------------------------------

    if not candidate["name"]:

        raise ValueError(
            "Candidate name could not be extracted."
        )

    if not candidate["skills"]:

        raise ValueError(
            "Candidate technical skills could not be extracted."
        )

    # --------------------------------------------------
    # Success
    # --------------------------------------------------

    print("=" * 80)
    print("✅ RESUME ANALYSIS COMPLETED")
    print("=" * 80)

    print(
        "Name:",
        candidate["name"]
    )

    print(
        "Role:",
        candidate["target_role"]
    )

    print(
        "Skills:",
        len(candidate["skills"])
    )

    print(
        "Experience:",
        len(candidate["experience"])
    )

    print(
        "Projects:",
        len(candidate["projects"])
    )

    print(
        "Certifications:",
        len(candidate["certifications"])
    )

    print("=" * 80)

    return candidate