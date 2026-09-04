import fitz
import streamlit as st


def extract_resume_text(uploaded_file):
    """
    Extract text from uploaded PDF resume.
    """

    if uploaded_file is None:
        st.error("Please upload a resume.")
        return ""

    try:
        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        resume_text = ""

        for page in pdf:
            resume_text += page.get_text()

        pdf.close()

        resume_text = resume_text.strip()

        print("=" * 80)
        print("📄 RESUME EXTRACTED")
        print("Characters:", len(resume_text))
        print("=" * 80)
        print(resume_text[:2000])
        print("=" * 80)

        if not resume_text:
            st.error("No text could be extracted from the resume.")
            return ""

        return resume_text

    except Exception as e:
        st.error(f"Unable to read the resume: {e}")
        return ""