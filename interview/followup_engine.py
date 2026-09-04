"""
Follow-up Engine

Responsible for:
1. Generating ONE follow-up question.
2. Focusing on missing concepts.
3. Keeping the same topic and difficulty.
"""

from config import client
from interview.interview_constants import MODEL_NAME


FOLLOWUP_PROMPT = """
You are an expert technical interviewer.

Generate ONE follow-up interview question.

Topic:
{topic}

Difficulty:
{difficulty}

Original Question:
{question}

Candidate Answer:
{answer}

Missing Concepts:
{missing_concepts}

Rules:

1. Ask ONLY ONE follow-up question.

2. The question must assess the missing concepts.

3. Keep the SAME difficulty.

4. Do NOT repeat the original question.

5. Do NOT provide explanations.

Return ONLY the follow-up question as plain text.
"""


def generate_followup(
    topic: str,
    difficulty: str,
    question: str,
    answer: str,
    missing_concepts: list,
) -> str:
    """
    Generate a single follow-up question.
    """

    prompt = FOLLOWUP_PROMPT.format(
        topic=topic,
        difficulty=difficulty,
        question=question,
        answer=answer,
        missing_concepts=", ".join(missing_concepts),
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text.strip()