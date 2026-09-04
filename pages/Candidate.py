import streamlit as st
import re

from resume.resume_parser import extract_resume_text
from resume.resume_analyzer import analyze_resume
from knowledge.knowledge_retriever import retrieve_knowledge
from interview.interview_engine import generate_interview
from interview.session import initialize_session, reset_interview
from evaluation.evaluation_engine import evaluate_answer
from interview.followup_engine import generate_followup
from database.database import interview_exists

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Candidate Dashboard",
    page_icon="👤",
    layout="wide"
)

initialize_session()

st.title("👤 Candidate Dashboard")

st.subheader("Candidate Information")

email = st.text_input(
    "Email Address",
    placeholder="Enter your email"
)

if not email:
    st.info("Please enter your email to continue.")
    st.stop()

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

if not re.match(email_pattern, email):
    st.error("Please enter a valid email address.")
    st.stop()

if interview_exists(email):
    st.error("This email has already completed the interview.")
    st.stop()
# -------------------------
# Upload Resume
# -------------------------

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_resume:

    # -------------------------
    # Resume Parsing
    # -------------------------

    with st.spinner("Extracting Resume..."):
        resume_text = extract_resume_text(uploaded_resume)

        print("=" * 80)
        print("RESUME LENGTH:", len(resume_text))
        print("=" * 80)
        print(resume_text[:3000])
        print("=" * 80)

    st.success("✅ Resume Extracted")

    # -------------------------
    # Resume Analysis
    # -------------------------

    with st.spinner("Analyzing Resume..."):

        candidate = analyze_resume(resume_text)
        print(type(candidate))
        print(candidate)

    st.success("✅ Resume Analyzed")

    st.subheader("Candidate Profile")

    st.success(f"👋 Welcome, {candidate['name']}")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🎯 Target Role")
        st.info(candidate["target_role"])

    with col2:

        st.markdown("### 🛠 Technical Skills")

        for skill in candidate["skills"]:

            st.success(skill)

    st.markdown("---")

    st.subheader("💼 Work Experience")

    if candidate["experience"]:
        for exp in candidate["experience"]:
            with st.expander(
                f"{exp.get('role', 'Unknown Role')} - {exp.get('company', 'Unknown Company')}"
            ):
                st.write(f"**Company:** {exp.get('company', 'N/A')}")
                st.write(f"**Role:** {exp.get('role', 'N/A')}")
                st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
                st.write(f"**Description:** {exp.get('description', 'N/A')}")

    else:
        st.info("No work experience found.")

    st.subheader("📂 Projects")

    if candidate["projects"]:

        for project in candidate["projects"]:

            with st.expander(project["title"], expanded=True):

                st.write(project["description"])

                st.markdown("**Technologies Used**")

                cols = st.columns(3)

                for index, tech in enumerate(project["technologies"]):

                    cols[index % 3].success(tech)

    else:

        st.info("No projects found.")

    st.markdown("---")

    st.subheader("🏆 Certifications")

    if candidate["certifications"]:

        for certificate in candidate["certifications"]:

            st.success(certificate)

    else:

        st.info("No certifications found.")

    # -------------------------
    # Knowledge Retrieval
    # -------------------------

    knowledge = retrieve_knowledge(candidate)

    if not st.session_state.questions:

        questions = generate_interview(knowledge)

        st.session_state.questions = questions

        st.session_state.candidate = candidate

        st.session_state.knowledge = knowledge

    questions = st.session_state.questions

    st.write(f"Found **{len(questions)}** Interview Questions")
    if len(questions) == 0:
        st.error(
            "No interview questions found.\n"
            "Please check the resume analysis or knowledge database."
        )
        st.stop()
    # -------------------------
    # Start Interview
    # -------------------------

    if not st.session_state.interview_started:

        if st.button("🚀 Start Interview"):

            st.session_state.interview_started = True

            st.session_state.questions = questions

            st.session_state.candidate = candidate

            st.session_state.knowledge = knowledge

            st.rerun()

    # -------------------------
    # Interview Started
    # -------------------------

    if st.session_state.interview_started:

        current = st.session_state.current_question

        total = len(st.session_state.questions)

        if len(st.session_state.questions) == 0:
            st.error("No interview questions were generated.")
            st.stop()

        if current >= len(st.session_state.questions):
            st.error("Current question index is out of range.")
            st.stop()

        question = st.session_state.questions[current]

        st.progress((current + 1) / total)

        st.subheader(f"🧠 Technical Interview")

        st.progress((current+1)/total)

        st.write(f"### Question {current+1} / {total}")

        col1,col2=st.columns(2)

        col1.metric("Topic",question["topic"])

        col2.metric("Difficulty",question["difficulty"].title())

        st.markdown("### Interview Question")

        st.info(question["question"])

        answer = st.text_area(

            "Your Answer",

            value="",

            height=180,

            key=f"answer_{current}"
        )

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter your answer.")
                st.stop()

            with st.spinner("Evaluating Answer..."):

                result = evaluate_answer(

                    question["question"],

                    answer

                )
            
            st.session_state.answers.append(answer)

            st.session_state.scores.append(result["score"])

            st.session_state.feedback.append(result["feedback"])

            st.session_state.strengths.append(
                result["strengths"]
            )

            st.session_state.missing_concepts.append(
                result["missing_concepts"]
            )

            st.success("Answer Evaluated")

            if result["needs_followup"]:

                followup = generate_followup(

                    question["question"],

                    answer,

                    result["missing_concepts"]

                )

                st.session_state.followup_question = followup

            else:

                st.session_state.followup_question = None

        if len(st.session_state.scores) > current:

            st.metric(
                "Score",
                f"{st.session_state.scores[current]}/10"
            )

            st.subheader("Feedback")
            st.write(st.session_state.feedback[current])

            st.subheader("Strengths")
            for item in st.session_state.strengths[current]:
                st.success(item)

            st.subheader("Missing Concepts")
            for concept in st.session_state.missing_concepts[current]:
                st.write(f"• {concept}")

            # -------------------------
            # Follow-up Question
            # -------------------------

            if st.session_state.followup_question:

                st.warning("Follow-up Question")

                st.info(st.session_state.followup_question)

                followup_answer = st.text_area(
                    "Follow-up Answer",
                    key=f"followup_{current}"
                )

                if st.button("Submit Follow-up"):

                    if not followup_answer.strip():
                        st.warning("Please enter your follow-up answer.")
                        st.stop()

                    followup_result = evaluate_answer(
                        st.session_state.followup_question,
                        followup_answer
                    )

                    st.metric(
                        "Follow-up Score",
                        f"{followup_result['score']}/10"
                    )

                    st.write(followup_result["feedback"])

                    st.session_state.followup_question = None

                    st.success("Follow-up Completed")

            # -------------------------
            # Next Question
            # -------------------------

            if st.button(
                "Next Question",
                disabled=st.session_state.followup_question is not None
            ):

                if current < total - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.interview_finished = True

                st.rerun()
    # -------------------------
    # Interview Finished
    # -------------------------

    if st.session_state.interview_finished:

        st.balloons()

        st.success("🎉 Interview Completed Successfully")

        st.write("Total Questions Answered")

        st.metric(
            "Questions",
            len(st.session_state.answers)
        )

        if st.session_state.scores:

            average = round(

                sum(st.session_state.scores)

                / len(st.session_state.scores),

                2

            )

        else:

            average = 0

        st.metric("Average Technical Score",f"{average}/10")
        if average>=8:

            st.success("Recommendation : Strong Hire")

        elif average>=6:

            st.warning("Recommendation : Hire")

        else:

            st.error("Recommendation : Needs Improvement")
