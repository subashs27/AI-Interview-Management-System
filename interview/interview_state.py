"""
Interview State

Stores the complete interview state in a single object.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from interview.interview_constants import (
    START_DIFFICULTY,
    MEDIUM_WEIGHT,
    TOTAL_MARKS,
    FOLLOWUP_WEIGHT
)


@dataclass
class InterviewState:

    # ==================================================
    # Interview Status
    # ==================================================

    interview_started: bool = False
    interview_finished: bool = False

    # ==================================================
    # Candidate Information
    # ==================================================

    candidate: Optional[Dict] = None
    knowledge: List[Dict] = field(default_factory=list)

    # ==================================================
    # Current Question
    # ==================================================

    current_question: Optional[Dict] = None
    current_topic: Optional[str] = None
    current_difficulty: str = START_DIFFICULTY
    current_weight: int = MEDIUM_WEIGHT
    question_number: int = 0

    # ==================================================
    # Marks
    # ==================================================

    remaining_marks: int = TOTAL_MARKS

    technical_marks: int = 0
    communication_marks: int = 0
    confidence_marks: int = 0

    overall_score: float = 0.0
    recommendation: str = ""

    # ==================================================
    # Adaptive Interview
    # ==================================================

    completion_mode: bool = False

    followup_required: bool = False
    followup_count: int = 0

    # ==================================================
    # History
    # ==================================================

    question_history: List[Dict] = field(
        default_factory=list
    )

    topic_history: List[str] = field(
        default_factory=list
    )

    answer_history: List[str] = field(
        default_factory=list
    )

    evaluation_history: List[Dict] = field(
        default_factory=list
    )

    followup_history: List[str] = field(
        default_factory=list
    )

    # ==================================================
    # Final Report
    # ==================================================

    interview_duration: float = 0.0

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )

    summary: str = ""

    # ==================================================
    # Voice
    # ==================================================

    audio_path: Optional[str] = None

    transcript: str = ""

    confidence_analysis: Dict = field(
        default_factory=dict
    )

    # ==================================================
    # Utility Methods
    # ==================================================

    def reset(self):
        """
        Reset the interview state.
        """

        self.__dict__.clear()

        self.__dict__.update(
            InterviewState().__dict__
        )

    # ==================================================
    # Question Management
    # ==================================================

    def add_question(self, question: Dict):
        """
        Store a newly generated question.

        A question can be either:

        Main question:
            weight = 5 / 10 / 20

        Follow-up question:
            weight = 10
            is_followup = True
        """

        self.current_question = question

        self.current_topic = question.get(
            "topic"
        )

        self.current_difficulty = question.get(
            "difficulty",
            self.current_difficulty
        )

        self.current_weight = question.get(
            "weight",
            self.current_weight
        )

        self.question_history.append(
            question
        )

        if self.current_topic:

            self.topic_history.append(
                self.current_topic
            )

        self.question_number += 1

        print(
            "Question Number Updated:",
            self.question_number
        )

    # ==================================================
    # Answer Management
    # ==================================================

    def add_answer(self, answer: str):
        """
        Store candidate answer.
        """

        self.answer_history.append(
            answer
        )

    # ==================================================
    # Evaluation Management
    # ==================================================

    def add_evaluation(self, evaluation: Dict):
        """
        Store evaluation and update performance scores.
        """

        self.evaluation_history.append(
            evaluation
        )

        self.technical_marks += evaluation.get(
            "technical_score",
            0
        )

        self.communication_marks += evaluation.get(
            "communication_score",
            0
        )

        self.confidence_marks += evaluation.get(
            "confidence_score",
            0
        )

    # ==================================================
    # Mark Management
    # ==================================================

    def reduce_marks(self, marks: int):
        """
        Reduce remaining interview marks.

        The value can never become negative.
        """

        if marks <= 0:
            return

        self.remaining_marks = max(
            0,
            self.remaining_marks - marks
        )

        print(
            "Marks Reduced:",
            marks
        )

        print(
            "Remaining Marks:",
            self.remaining_marks
        )

    # ==================================================
    # Follow-up Mark Management
    # ==================================================

    def add_followup_marks(self):
        """
        Deduct the fixed 10 marks allocated
        to a follow-up question.
        """

        self.reduce_marks(
            FOLLOWUP_WEIGHT
        )

        self.followup_count += 1

        print(
            "Follow-up Marks:",
            FOLLOWUP_WEIGHT
        )

        print(
            "Follow-up Count:",
            self.followup_count
        )

    # ==================================================
    # Completion Mode
    # ==================================================

    def enable_completion_mode(self):
        """
        Enable completion mode.

        Once enabled, follow-up questions
        must not be generated.
        """

        self.completion_mode = True

        self.followup_required = False

        print(
            "Completion Mode: ENABLED"
        )

    # ==================================================
    # Follow-up Status
    # ==================================================

    def set_followup_required(
        self,
        required: bool
    ):
        """
        Store follow-up decision.
        """

        self.followup_required = required

    # ==================================================
    # Interview Completion
    # ==================================================

    def finish(self):
        """
        Mark interview as completed.
        """

        self.interview_finished = True

        self.interview_started = False

        self.followup_required = False

        print(
            "Interview Finished"
        )

        print(
            "Final Remaining Marks:",
            self.remaining_marks
        )

    # ==================================================
    # Utility Information
    # ==================================================

    def get_total_questions(self):
        """
        Return total questions asked.

        This includes main questions and
        follow-up questions.
        """

        return len(
            self.question_history
        )

    def get_total_main_questions(self):
        """
        Return number of main questions only.
        """

        return sum(
            1
            for question in self.question_history
            if not question.get(
                "is_followup",
                False
            )
        )

    def get_total_followups(self):
        """
        Return number of follow-up questions.
        """

        return sum(
            1
            for question in self.question_history
            if question.get(
                "is_followup",
                False
            )
        )

    def get_total_answers(self):
        """
        Return total submitted answers.
        """

        return len(
            self.answer_history
        )

    def get_last_question(self):
        """
        Return current question.
        """

        return self.current_question

    def get_last_evaluation(self):
        """
        Return latest evaluation.
        """

        if not self.evaluation_history:

            return None

        return self.evaluation_history[-1]