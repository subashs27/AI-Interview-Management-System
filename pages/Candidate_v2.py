import streamlit as st
import re

from database.schema import create_tables
from interview.interview_manager import InterviewManager
from interview.session import get_state

from resume.resume_parser import extract_resume_text
from resume.resume_analyzer import analyze_resume
from knowledge.knowledge_retriever import retrieve_knowledge

from voice.recorder import record_voice
from voice.speech_to_text import speech_to_text
from voice.voice_analysis import (
    analyze_voice,
    speaking_rate
)

st.set_page_config(
    page_title="AI Interview",
    layout="wide"
)
create_tables()

st.title("🎤 AI Interview System")

manager = InterviewManager()
state = get_state()

EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None

# =====================================================
# Resume Upload
# =====================================================

if not state.interview_started:
    st.subheader("Candidate Details")

    name = st.text_input("Full Name *")

    email = st.text_input("Email Address *")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if uploaded_file:

        with st.spinner("Parsing Resume..."):
            resume_text = extract_resume_text(uploaded_file)

        with st.spinner("Analyzing Resume..."):
            candidate = analyze_resume(resume_text)

        st.success("Resume analyzed successfully")

        st.subheader("Candidate Profile")
        st.write(candidate)

        if st.button("Start Interview"):
            if not name.strip():
                st.error("Please enter your name.")
                st.stop()

            if not email.strip():
                st.error("Please enter your email.")
                st.stop()

            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
                st.stop()
            
            candidate["name"] = name
            candidate["email"] = email

            with st.spinner("Retrieving Knowledge..."):
                knowledge = retrieve_knowledge(candidate)

            manager.start(candidate, knowledge)

            st.rerun()

# =====================================================
# Interview
# =====================================================

else:

    if not manager.is_finished():

        question = manager.get_current_question()

        st.subheader(f"Question {state.question_number}")

        st.info(question["question"])

        st.markdown("---")

        st.subheader("🎤 Voice Answer")

        audio = record_voice()

        # Process newly recorded audio
        if audio:

            with st.spinner("Transcribing Voice..."):
                st.session_state.transcript = speech_to_text(audio)

            metrics = analyze_voice(audio)

            metrics["speaking_rate"] = speaking_rate(
                st.session_state.transcript,
                metrics["duration"]
            )

            st.session_state.voice_metrics = metrics

        # Display transcript if available
        if "transcript" in st.session_state:

            st.success("Voice recorded successfully")

            st.subheader("Review Your Answer")

            st.session_state.transcript = st.text_area(
                "You can edit the transcript before submitting",
                value=st.session_state.transcript,
                height=180
            )

            if st.button(
                "Submit Voice Answer",
                use_container_width=True
            ):

                try:

                    with st.spinner("Evaluating Answer..."):

                        result = manager.submit_answer(
                            st.session_state.transcript
                        )

                    st.success("✅ submit_answer completed")
                    st.write("Question Number:", state.question_number)
                    st.write("History:", len(state.question_history))

                    # Clear previous answer
                    del st.session_state.transcript
                    del st.session_state.voice_metrics

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

                    import traceback

                    st.code(traceback.format_exc())


    else:

        report = manager.get_report()

        st.success("🎉 Interview Completed")

        st.title("AI Interview Report")

        # -------------------------------
        # Candidate Details
        # -------------------------------

        st.subheader("👤 Candidate Details")

        c1, c2 = st.columns(2)

        with c1:
            st.write("**Name:**", report["candidate"].get("name", "N/A"))
            st.write("**Role:**", report["candidate"].get("target_role", "N/A"))

        with c2:
            st.write("**Interview Date:**", report["date"])
            st.write("**Questions:**", report["questions"])

        st.divider()

        # -------------------------------
        # Performance
        # -------------------------------

        st.subheader("📊 Performance Summary")

        a, b, c, d = st.columns(4)

        a.metric("Overall", f'{report["overall_score"]}%')

        b.metric("Technical", f'{report["technical"]}/10')

        c.metric("Communication", f'{report["communication"]}/10')

        d.metric("Confidence", f'{report["confidence"]}/10')

        st.progress(report["overall_score"] / 100)

        st.success(
            f"Recommendation : **{report['recommendation']}**"
        )

        st.divider()

        # -------------------------------
        # Strengths
        # -------------------------------

        st.subheader("💪 Strengths")

        if report["strengths"]:

            for item in report["strengths"]:
                st.write("✅", item)

        else:
            st.write("No strengths identified.")

        # -------------------------------
        # Weaknesses
        # -------------------------------

        st.subheader("📚 Areas for Improvement")

        if report["weaknesses"]:

            for item in report["weaknesses"]:
                st.write("🔸", item)

        else:
            st.write("No major weaknesses identified.")

        st.divider()

        # -------------------------------
        # AI Summary
        # -------------------------------

        st.subheader("🤖 AI Summary")

        st.info(report["summary"])

        st.divider()

        # -------------------------------
        # Question-wise Analysis
        # -------------------------------

        st.subheader("📝 Question-wise Analysis")

        for q in report["question_details"]:

            with st.expander(
                f'Q{q["question_no"]} - {q["topic"]}'
            ):

                st.write("**Difficulty:**", q["difficulty"])

                st.write("**Question:**")
                st.write(q["question"])

                st.write("**Your Answer:**")
                st.write(q["answer"])

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Technical",
                    f'{q["technical"]}/10'
                )

                col2.metric(
                    "Communication",
                    f'{q["communication"]}/10'
                )

                col3.metric(
                    "Confidence",
                    f'{q["confidence"]}/10'
                )

                st.write("**Feedback:**")
                st.success(q["feedback"])

        st.divider()

        if st.button(
            "Restart Interview",
            use_container_width=True
        ):

            state.reset()

            st.rerun()