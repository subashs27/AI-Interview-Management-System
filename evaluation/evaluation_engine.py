"""
Evaluation Engine

Evaluates candidate answers using Gemini.

Returns:
- Technical score
- Communication score
- Confidence score
- Performance
- Feedback
- Strengths
- Missing concepts
- Follow-up decision
- Follow-up question

Evaluation and follow-up generation are performed
in a SINGLE Gemini request.
"""

import json
import re

from google.genai import types

from config import client
from evaluation.evaluation_prompt import EVALUATION_PROMPT
from interview.interview_constants import (
    MODEL_NAME,
    FOLLOWUP_TECHNICAL_THRESHOLD
)


# =====================================================
# Required Fields
# =====================================================

REQUIRED_FIELDS = {

    "technical_score",

    "communication_score",

    "confidence_score",

    "performance",

    "feedback",

    "strengths",

    "missing_concepts",

    "followup_required",

    "followup_question"

}


# =====================================================
# JSON Cleaning
# =====================================================

def clean_json_response(text: str):

    if not text:
        raise ValueError(
            "Gemini returned an empty response."
        )

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


# =====================================================
# Validate Response
# =====================================================

def validate_response(data):

    if not isinstance(data, dict):

        raise ValueError(
            "Gemini response is not a JSON object."
        )

    missing = REQUIRED_FIELDS - set(data.keys())

    if missing:

        raise ValueError(
            f"Missing fields: {missing}"
        )


# =====================================================
# Follow-up Decision
# =====================================================
    from interview.interview_constants import (
        MODEL_NAME,
        FOLLOWUP_TECHNICAL_THRESHOLD
    )
    
    technical_score = int(data["technical_score"])

    # Above 70% means 8/10, 9/10 or 10/10
    data["followup_required"] = (
        technical_score > FOLLOWUP_TECHNICAL_THRESHOLD
    )

    if not data["followup_required"]:
        data["followup_question"] = ""

# =====================================================
# Local Fallback Evaluation
# =====================================================

def fallback_evaluation(question, answer):
    """
    Local evaluation used when Gemini is unavailable.
    """

    answer = answer.strip()
    question = question.strip()

    if not answer:
        return {
            "technical_score": 0,
            "communication_score": 0,
            "confidence_score": 0,
            "performance": "weak",
            "feedback": "No answer was provided.",
            "strengths": [],
            "missing_concepts": ["Answer required"],
            "followup_required": False,
            "followup_question": ""
        }

    # Basic answer-quality evaluation
    words = answer.split()
    word_count = len(words)

    # Technical score
    if word_count >= 80:
        technical_score = 8
    elif word_count >= 40:
        technical_score = 7
    elif word_count >= 20:
        technical_score = 6
    else:
        technical_score = 4

    # Communication score
    if word_count >= 50:
        communication_score = 8
    elif word_count >= 25:
        communication_score = 7
    elif word_count >= 10:
        communication_score = 6
    else:
        communication_score = 4

    # Confidence score
    if word_count >= 50:
        confidence_score = 8
    elif word_count >= 25:
        confidence_score = 7
    else:
        confidence_score = 5

    if technical_score >= 8:
        performance = "excellent"
    elif technical_score >= 5:
        performance = "average"
    else:
        performance = "weak"

    return {
        "technical_score": technical_score,
        "communication_score": communication_score,
        "confidence_score": confidence_score,
        "performance": performance,
        "feedback": (
            "Answer evaluated using the local backup "
            "evaluation system because the AI evaluation "
            "service was temporarily unavailable."
        ),
        "strengths": [
            "Answer provided",
            "Relevant explanation attempted",
            "Communication assessed successfully"
        ],
        "missing_concepts": [],
        "followup_required": False,
        "followup_question": ""
    }

# =====================================================
# Evaluate Answer
# =====================================================

def evaluate_answer(
    question,
    answer
):

    prompt = (

        EVALUATION_PROMPT

        .replace(
            "<<QUESTION>>",
            question
        )

        .replace(
            "<<ANSWER>>",
            answer
        )

    )

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                temperature=0

            )

        )

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            print("=" * 80)
            print("⚠️ GEMINI QUOTA EXCEEDED")
            print("Using local fallback evaluation.")
            print("=" * 80)

            return fallback_evaluation(
                question,
                answer
            )

        raise RuntimeError(
            f"Gemini evaluation failed: {e}"
        ) from e

        # ---------------------------------------------
        # Other Gemini errors
        # ---------------------------------------------

        raise RuntimeError(

            f"Gemini evaluation failed: {e}"

        ) from e


    # =================================================
    # Parse Response
    # =================================================

    cleaned = clean_json_response(
        response.text
    )

    print("=" * 80)
    print("EVALUATION RESPONSE")
    print("=" * 80)
    print(cleaned)
    print("=" * 80)

    try:

        data = json.loads(
            cleaned
        )

    except json.JSONDecodeError as e:

        raise RuntimeError(

            "Gemini returned invalid evaluation JSON."

        ) from e


    # =================================================
    # Validate
    # =================================================

    validate_response(
        data
    )


    # =================================================
    # Normalize Follow-up
    # =================================================

    data["followup_required"] = bool(
        data["followup_required"]
    )

    data["followup_question"] = (

        str(
            data.get(
                "followup_question",
                ""
            )
        ).strip()

    )


    # Safety rule:
    # If Gemini says follow-up is required but
    # doesn't provide a question, disable follow-up.

    if (

        data["followup_required"]

        and not data["followup_question"]

    ):

        data["followup_required"] = False


    return data