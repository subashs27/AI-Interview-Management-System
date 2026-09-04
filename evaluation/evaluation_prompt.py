"""
Prompt used to evaluate candidate answers.

The model MUST return ONLY valid JSON.
No markdown.
No explanations.
No additional text.
"""

from interview.interview_constants import (
    MAX_TECHNICAL_SCORE,
    MAX_COMMUNICATION_SCORE,
    MAX_CONFIDENCE_SCORE,
)

EVALUATION_PROMPT = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer objectively.

-------------------------------------------------
Question:

<<QUESTION>>

-------------------------------------------------

Candidate Answer:

<<ANSWER>>

-------------------------------------------------

Evaluate the answer on the following criteria.

1. Technical Accuracy

- Correctness
- Completeness
- Depth of knowledge

Score:
0 to {MAX_TECHNICAL_SCORE}

-------------------------------------------------

2. Communication

Evaluate:

- Clarity
- Structure
- Grammar
- Explanation Quality

Score:
0 to {MAX_COMMUNICATION_SCORE}

-------------------------------------------------

3. Confidence

Evaluate:

- Confidence
- Logical Flow
- Technical Understanding

Score:
0 to {MAX_CONFIDENCE_SCORE}

-------------------------------------------------

Determine performance:

technical_score >= 8
excellent

technical_score >= 5
average

technical_score < 5
weak

-------------------------------------------------

Identify EXACTLY 3 strengths.

-------------------------------------------------

Identify EXACTLY 3 missing concepts.

-------------------------------------------------

FOLLOW-UP DECISION

Determine whether the candidate needs a follow-up
question based on the quality of the answer.

Set:

followup_required = true

ONLY when an important concept is missing,
unclear, incorrect, or insufficiently explained.

Set:

followup_required = false

when the answer is sufficiently complete.

-------------------------------------------------

FOLLOW-UP QUESTION

If followup_required is true:

Generate ONE short, relevant follow-up question
based specifically on the candidate's answer
and the missing concepts.

The follow-up question must:

- Stay within the same topic
- Test the missing or weak concept
- Be appropriate for the candidate's current difficulty
- Not repeat the original question
- Be technically relevant to the target interview
- Be concise

If followup_required is false:

Return an empty string for followup_question.

-------------------------------------------------

Provide short constructive feedback.

-------------------------------------------------

Return ONLY valid JSON.

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,

    "performance": "",

    "feedback": "",

    "strengths": [
        "",
        "",
        ""
    ],

    "missing_concepts": [
        "",
        "",
        ""
    ],

    "followup_required": false,

    "followup_question": ""
}}

Return ONLY JSON.
Do NOT use markdown.
Do NOT explain anything.
"""