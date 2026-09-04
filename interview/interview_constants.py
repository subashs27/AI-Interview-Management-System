"""
Centralized constants for the AI Interview System.

Do not hardcode interview values anywhere else.
Import constants from this file.
"""

# =====================================================
# Interview Marks
# =====================================================

TOTAL_MARKS = 40

EASY_WEIGHT = 5
MEDIUM_WEIGHT = 10
HARD_WEIGHT = 20

FOLLOWUP_WEIGHT = 10

QUESTION_WEIGHTS = {
    "easy": EASY_WEIGHT,
    "medium": MEDIUM_WEIGHT,
    "hard": HARD_WEIGHT
}

# =====================================================
# Difficulty Levels
# =====================================================

EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

DIFFICULTIES = [
    EASY,
    MEDIUM,
    HARD
]

START_DIFFICULTY = MEDIUM

# =====================================================
# Performance Levels
# =====================================================

EXCELLENT = "excellent"
AVERAGE = "average"
WEAK = "weak"

# =====================================================
# Completion Rules
# =====================================================

COMPLETION_MODE_THRESHOLD = 20

# Remaining Marks Mapping
#
# 20 -> Hard
# 15 -> Medium + Easy
# 10 -> Medium
# 5  -> Easy
#

COMPLETION_RULES = {
    20: [HARD],
    15: [MEDIUM, EASY],
    10: [MEDIUM],
    5: [EASY]
}

# =====================================================
# Evaluation
# =====================================================

MAX_TECHNICAL_SCORE = 10
MAX_COMMUNICATION_SCORE = 10
MAX_CONFIDENCE_SCORE = 10

FOLLOWUP_TECHNICAL_THRESHOLD = 7

MAX_FOLLOWUPS_PER_QUESTION = 1
# =====================================================
# Recommendation
# =====================================================

SELECTED = "Selected"

REJECTED = "Rejected"

NEEDS_IMPROVEMENT = "Needs Improvement"

# =====================================================
# Follow-up
# =====================================================

MAX_FOLLOWUPS_PER_QUESTION = 1

# =====================================================
# LLM
# =====================================================

MODEL_NAME = "gemini-2.5-flash"