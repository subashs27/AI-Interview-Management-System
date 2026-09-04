import streamlit as st

from role_topic_generator import generate_topics
from generator import generate_knowledge

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠",
    layout="wide"
)

st.title("🛠 AI Interview Admin Dashboard")

st.markdown("Generate a knowledge base for a specific job role.")

# -----------------------------
# Role Selection
# -----------------------------

roles = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Python Developer",
    "Backend Developer",
    "Java Developer",
    "Data Analyst",
    "Data Scientist",
    "Full Stack Developer",
    "Software Engineer",
    "Custom"
]

selected_role = st.selectbox(
    "Select Target Role",
    roles
)

if selected_role == "Custom":
    selected_role = st.text_input("Enter Role Name")

# -----------------------------
# Generate Button
# -----------------------------

generate = st.button(
    "🚀 Generate Knowledge Base",
    use_container_width=True
)

if generate:

    if not selected_role:

        st.warning("Please enter a role.")

    else:

        with st.spinner("Generating Interview Topics..."):

            topics = generate_topics(selected_role)

        st.success(f"Generated {len(topics)} Topics")

        progress = st.progress(0)

        status = st.empty()

        failed_topics = []
        success_count = 0

        for i, topic in enumerate(topics):

            status.write(f"Generating: {topic['topic']}")

            knowledge = generate_knowledge(topic)

            if knowledge is None:

                failed_topics.append(topic["topic"])

            else:

                success_count += 1

            progress.progress((i + 1) / len(topics))

        status.success("✅ Knowledge Base Generation Completed!")

        st.success(f"Successfully Generated: {success_count}")

        if failed_topics:

            st.warning(
                f"Failed to Generate: {len(failed_topics)} Topic(s)"
            )

            st.write("### Failed Topics")

            for topic in failed_topics:

                st.write(f"• {topic}")

        else:

            st.success("🎉 All topics generated successfully!")

        st.balloons()