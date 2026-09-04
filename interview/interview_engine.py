"""
Interview Question Generator

Responsible for:
1. Selecting a topic
2. Selecting a question
3. Avoiding duplicate questions
4. Returning ONE question
"""

import random

from interview.interview_constants import QUESTION_WEIGHTS


def _normalize_knowledge(knowledge):
    """
    Normalize knowledge into a flat list of question records.

    Expected input examples:

    [
        {
            "topic":"Python",
            "questions":[
                {
                    "difficulty":"easy",
                    "question":"What is Python?"
                }
            ]
        }
    ]

    OR already flattened.
    """

    records = []

    for item in knowledge:

        topic = item.get("topic", "General")

        questions = item.get("questions")

        if questions:

            for q in questions:

                records.append(
                    {
                        "topic": topic,
                        "difficulty": q["difficulty"].lower(),
                        "question": q["question"]
                    }
                )

        else:

            records.append(
                {
                    "topic": item.get("topic", "General"),
                    "difficulty": item["difficulty"].lower(),
                    "question": item["question"]
                }
            )

    return records


def generate_question(
    knowledge,
    difficulty,
    question_history
):
    """
    Generate ONE question.

    Parameters
    ----------
    knowledge : list

    difficulty : easy | medium | hard

    question_history : previously asked questions

    Returns
    -------
    dict
    """

    records = _normalize_knowledge(knowledge)

    asked_questions = {
        q["question"]
        for q in question_history
    }

    candidates = [

        q

        for q in records

        if q["difficulty"] == difficulty

        and q["question"] not in asked_questions

    ]

    if not candidates:

        raise ValueError(

            f"No unused {difficulty} questions available."

        )

    selected = random.choice(candidates)

    return {

        "topic": selected["topic"],

        "difficulty": difficulty,

        "weight": QUESTION_WEIGHTS[difficulty],

        "question": selected["question"]

    }


def has_questions(
    knowledge,
    difficulty,
    question_history
):
    """
    Check whether unused questions exist.
    """

    records = _normalize_knowledge(knowledge)

    asked = {

        q["question"]

        for q in question_history

    }

    return any(

        q["difficulty"] == difficulty

        and q["question"] not in asked

        for q in records

    )