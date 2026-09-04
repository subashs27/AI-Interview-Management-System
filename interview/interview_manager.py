"""
Interview Manager

Controls the complete interview lifecycle.
"""

from datetime import datetime

from interview.session import get_state
from interview.interview_engine import generate_question
from interview.adaptive_engine import decide_next_step
from evaluation.evaluation_engine import evaluate_answer


class InterviewManager:

    def __init__(self):

        self.state = get_state()

    # =====================================================
    # Start Interview
    # =====================================================

    def start(self, candidate, knowledge):

        self.state.reset()

        self.state.interview_started = True

        self.state.candidate = candidate

        self.state.knowledge = knowledge

        # ---------------------------------------------
        # Generate First Main Question
        # ---------------------------------------------

        question = generate_question(

            knowledge=knowledge,

            difficulty=self.state.current_difficulty,

            question_history=self.state.question_history

        )

        question["is_followup"] = False

        self.state.add_question(question)

        return question

    # =====================================================
    # Current Question
    # =====================================================

    def get_current_question(self):

        return self.state.current_question

    # =====================================================
    # Submit Answer
    # =====================================================

    def submit_answer(self, answer):

        print("=" * 80)
        print("STEP 1: submit_answer() called")

        question = self.state.current_question

        print("Current Question:")
        print(question)

        # ---------------------------------------------
        # Store Answer
        # ---------------------------------------------

        self.state.add_answer(answer)

        print("STEP 2: Answer stored")

        # ---------------------------------------------
        # Evaluate Answer
        # ---------------------------------------------

        evaluation = evaluate_answer(

            question=question["question"],

            answer=answer

        )

        print("STEP 3: Evaluation completed")

        print(evaluation)

        self.state.add_evaluation(
            evaluation
        )

        # =================================================
        # MARK CALCULATION
        # =================================================

        # ---------------------------------------------
        # Main Question
        # ---------------------------------------------

        if not question.get(
            "is_followup",
            False
        ):

            question_weight = question.get(
                "weight",
                0
            )

            self.state.reduce_marks(
                question_weight
            )

            print(
                "Main Question Marks:",
                question_weight
            )

        # ---------------------------------------------
        # Follow-up Question
        # ---------------------------------------------

        else:

            self.state.add_followup_marks()

            print(
                "Follow-up Marks:",
                10
            )

        print(
            "Remaining Marks:",
            self.state.remaining_marks
        )

        # =================================================
        # Adaptive Decision
        # =================================================

        decision = decide_next_step(

            self.state,

            evaluation

        )

        print("STEP 4: Decision")

        print(decision)

        # =================================================
        # Next Question
        # =================================================

        next_question = self._next_question(
            decision
        )

        print("STEP 5: Next Question")

        print(next_question)

        return next_question

    # =====================================================
    # Decide Next Question
    # =====================================================

    def _next_question(self, decision):

        print("=" * 80)
        print("ENTERED _next_question()")

        # =================================================
        # Interview Completed
        # =================================================

        if self.state.remaining_marks <= 0:

            self.state.finish()

            return None

        # =================================================
        # Follow-up Question
        # =================================================

        # Follow-up is allowed ONLY when:
        #
        # 1. We are NOT in completion mode
        # 2. Current question is a MAIN question
        # 3. Adaptive engine requested a follow-up
        # 4. Gemini supplied a follow-up question
        #
        # Follow-up = 10 marks

        if (
            not self.state.completion_mode
            and not self.state.current_question.get(
                "is_followup",
                False
            )
            and decision.get(
                "followup_required",
                False
            )
        ):

            followup = self.state.evaluation_history[-1].get(
                "followup_question",
                ""
            )

            if followup:

                # -----------------------------------------
                # Make sure enough marks remain
                # -----------------------------------------

                if self.state.remaining_marks >= 10:

                    # -------------------------------------
                    # Deduct follow-up marks
                    # -------------------------------------

                    self.state.add_followup_marks()

                    # -------------------------------------
                    # Create Follow-up Question
                    # -------------------------------------

                    question = {

                        "topic":
                            self.state.current_topic,

                        "difficulty":
                            self.state.current_difficulty,

                        "weight":
                            10,

                        "question":
                            followup,

                        "is_followup":
                            True

                    }

                    self.state.followup_history.append(
                        followup
                    )

                    self.state.add_question(
                        question
                    )

                    print(
                        "Follow-up Question:"
                    )

                    print(
                        followup
                    )

                    print(
                        "Follow-up Weight: 10"
                    )

                    print(
                        "Remaining Marks:",
                        self.state.remaining_marks
                    )

                    return question

                else:

                    print(
                        "Not enough marks for follow-up."
                    )

        # =================================================
        # Completion Mode
        # =================================================

        if decision.get(
            "completion_mode",
            False
        ):

            questions = decision.get(
                "questions",
                []
            )

            if not questions:

                print(
                    "No completion question available."
                )

                self.state.finish()

                return None

            difficulty = questions[0]

        # =================================================
        # Adaptive Main Question
        # =================================================

        else:

            difficulty = decision.get(
                "next_difficulty"
            )

            if not difficulty:

                print(
                    "No next difficulty available."
                )

                self.state.finish()

                return None

        # =================================================
        # Generate Main Question
        # =================================================

        question = generate_question(

            knowledge=self.state.knowledge,

            difficulty=difficulty,

            question_history=self.state.question_history

        )

        question["is_followup"] = False

        self.state.current_difficulty = (
            difficulty
        )

        self.state.current_weight = (
            question["weight"]
        )

        self.state.add_question(
            question
        )

        print(
            "Generated Main Question:"
        )

        print(
            question
        )

        print(
            "Main Question Weight:",
            question["weight"]
        )

        print(
            "Remaining Marks:",
            self.state.remaining_marks
        )

        return question

    # =====================================================
    # Status
    # =====================================================

    def is_finished(self):

        return self.state.interview_finished

    # =====================================================
    # Report
    # =====================================================

    def get_report(self):

        total_questions = (
            len(
                self.state.question_history
            )
        )

        if total_questions == 0:

            total_questions = 1

        # =================================================
        # Performance Scores
        # =================================================

        technical = round(

            self.state.technical_marks
            / total_questions,

            2

        )

        communication = round(

            self.state.communication_marks
            / total_questions,

            2

        )

        confidence = round(

            self.state.confidence_marks
            / total_questions,

            2

        )

        overall = round(

            (
                technical
                + communication
                + confidence
            )
            / 30
            * 100,

            2

        )

        # =================================================
        # Recommendation
        # =================================================

        if overall >= 85:

            recommendation = (
                "Outstanding Candidate"
            )

        elif overall >= 75:

            recommendation = "Selected"

        elif overall >= 60:

            recommendation = (
                "Needs Improvement"
            )

        else:

            recommendation = "Rejected"

        # =================================================
        # Strengths / Weaknesses
        # =================================================

        strengths = set()

        weaknesses = set()

        for evaluation in (
            self.state.evaluation_history
        ):

            for item in evaluation.get(
                "strengths",
                []
            ):

                strengths.add(item)

            for item in evaluation.get(
                "missing_concepts",
                []
            ):

                weaknesses.add(item)

        # =================================================
        # Question Details
        # =================================================

        question_details = []

        for i in range(
            len(
                self.state.question_history
            )
        ):

            question = (
                self.state.question_history[i]
            )

            answer = (

                self.state.answer_history[i]

                if i < len(
                    self.state.answer_history
                )

                else ""

            )

            evaluation = (

                self.state.evaluation_history[i]

                if i < len(
                    self.state.evaluation_history
                )

                else {}

            )

            question_details.append({

                "question_no":
                    i + 1,

                "topic":
                    question.get(
                        "topic",
                        "General"
                    ),

                "difficulty":
                    question.get(
                        "difficulty",
                        ""
                    ),

                "question":
                    question.get(
                        "question",
                        ""
                    ),

                "answer":
                    answer,

                "is_followup":
                    question.get(
                        "is_followup",
                        False
                    ),

                "weight":
                    question.get(
                        "weight",
                        0
                    ),

                "technical":
                    evaluation.get(
                        "technical_score",
                        0
                    ),

                "communication":
                    evaluation.get(
                        "communication_score",
                        0
                    ),

                "confidence":
                    evaluation.get(
                        "confidence_score",
                        0
                    ),

                "feedback":
                    evaluation.get(
                        "feedback",
                        ""
                    )

            })

        # =================================================
        # AI Summary
        # =================================================

        summary = (

            f"The candidate scored "
            f"{overall}% overall. "

            f"Technical knowledge was "
            f"{technical}/10, "

            f"communication was "
            f"{communication}/10 "

            f"and confidence was "
            f"{confidence}/10."

        )

        # =================================================
        # Final Report
        # =================================================

        return {

            "candidate":
                self.state.candidate,

            "date":
                datetime.now().strftime(
                    "%d-%m-%Y %I:%M %p"
                ),

            "overall_score":
                overall,

            "technical":
                technical,

            "communication":
                communication,

            "confidence":
                confidence,

            "recommendation":
                recommendation,

            "questions":
                total_questions,

            "main_questions":
                self.state.get_total_main_questions(),

            "followups":
                self.state.get_total_followups(),

            "total_followup_marks":
                self.state.followup_count * 10,

            "remaining_marks":
                self.state.remaining_marks,

            "strengths":
                sorted(
                    list(strengths)
                ),

            "weaknesses":
                sorted(
                    list(weaknesses)
                ),

            "summary":
                summary,

            "question_details":
                question_details

        }