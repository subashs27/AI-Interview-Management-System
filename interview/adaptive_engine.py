"""
Adaptive Interview Engine

Responsible for:
1. Difficulty progression
2. Completion mode
3. Remaining marks
4. Follow-up decision
"""

from interview.interview_constants import (
    EASY,
    MEDIUM,
    HARD,
    COMPLETION_MODE_THRESHOLD,
    COMPLETION_RULES,
    EXCELLENT,
    WEAK,
    QUESTION_WEIGHTS,
    FOLLOWUP_TECHNICAL_THRESHOLD,
)


# =====================================================
# Difficulty Progression
# =====================================================

def get_next_difficulty(
    current_difficulty: str,
    performance: str
) -> str:
    """
    Decide the next main-question difficulty.

    Excellent:
        Easy   -> Medium
        Medium -> Hard
        Hard   -> Hard

    Weak:
        Hard   -> Medium
        Medium -> Easy
        Easy   -> Easy

    Average:
        Keep the same difficulty.
    """

    if performance == EXCELLENT:

        if current_difficulty == EASY:
            return MEDIUM

        if current_difficulty == MEDIUM:
            return HARD

        return HARD

    elif performance == WEAK:

        if current_difficulty == HARD:
            return MEDIUM

        if current_difficulty == MEDIUM:
            return EASY

        return EASY

    # Average
    return current_difficulty


# =====================================================
# Completion Questions
# =====================================================

def get_completion_questions(
    remaining_marks: int
):
    """
    Decide the main question(s) required to
    complete the remaining marks.

    Rules:

        20 -> Hard
        15 -> Medium + Easy
        10 -> Medium
         5 -> Easy
    """

    return COMPLETION_RULES.get(
        remaining_marks,
        []
    )


# =====================================================
# Follow-up Decision
# =====================================================

def should_ask_followup(
    state,
    evaluation: dict
) -> bool:
    """
    Decide whether a follow-up question should
    be asked.

    Follow-up conditions:

    1. Must NOT be in completion mode.
    2. Remaining marks must be greater than 20.
    3. Current question must be a main question.
    4. Technical score must be above 70%.
       With a 10-point technical score:
       8, 9, or 10 qualifies.
    5. Maximum one follow-up per main question.
    """

    # ---------------------------------------------
    # Completion mode = NO FOLLOW-UP
    # ---------------------------------------------

    if state.completion_mode:
        return False

    # ---------------------------------------------
    # Remaining marks <= 20 = NO FOLLOW-UP
    # ---------------------------------------------

    if state.remaining_marks <= COMPLETION_MODE_THRESHOLD:
        return False

    # ---------------------------------------------
    # Follow-up cannot follow another follow-up
    # ---------------------------------------------

    current_question = state.current_question

    if not current_question:
        return False

    if current_question.get(
        "is_followup",
        False
    ):
        return False

    # ---------------------------------------------
    # Maximum one follow-up per main question
    # ---------------------------------------------

    if state.followup_count >= 1:

        # This is a global safety check.
        # InterviewManager will reset/use the
        # appropriate main-question logic.
        pass

    # ---------------------------------------------
    # Technical Score
    # ---------------------------------------------

    technical_score = int(
        evaluation.get(
            "technical_score",
            0
        )
    )

    # ---------------------------------------------
    # Above 70% = 8/10, 9/10, 10/10
    # ---------------------------------------------

    return (
        technical_score
        > FOLLOWUP_TECHNICAL_THRESHOLD
    )


# =====================================================
# Main Decision Function
# =====================================================

def decide_next_step(
    state,
    evaluation: dict
):
    """
    Main adaptive decision function.

    Priority:

    1. Completion mode
    2. Follow-up decision
    3. Adaptive difficulty
    """

    performance = evaluation.get(
        "performance",
        ""
    )

    # =================================================
    # COMPLETION MODE
    # =================================================

    if (
        state.remaining_marks
        <= COMPLETION_MODE_THRESHOLD
    ):

        state.enable_completion_mode()

        return {

            "completion_mode": True,

            "questions": get_completion_questions(
                state.remaining_marks
            ),

            # IMPORTANT:
            # No follow-up is allowed here.
            "followup_required": False,

            "next_difficulty": None,

            "question_weight": 0

        }

    # =================================================
    # FOLLOW-UP
    # =================================================

    followup_required = should_ask_followup(
        state,
        evaluation
    )

    if followup_required:

        return {

            "completion_mode": False,

            "next_difficulty": None,

            "question_weight": 0,

            "followup_required": True

        }

    # =================================================
    # ADAPTIVE MAIN QUESTION
    # =================================================

    next_difficulty = get_next_difficulty(

        state.current_difficulty,

        performance

    )

    return {

        "completion_mode": False,

        "next_difficulty": next_difficulty,

        "question_weight": QUESTION_WEIGHTS[
            next_difficulty
        ],

        "followup_required": False

    }