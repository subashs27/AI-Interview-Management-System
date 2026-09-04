"""
Speech To Text

Converts recorded audio into text using Gemini.
"""

import tempfile
import os

from config import client
from interview.interview_constants import MODEL_NAME


TRANSCRIPTION_PROMPT = """
You are an expert speech transcription system.

Transcribe the spoken interview answer accurately.

Rules:

- Return ONLY the spoken text.
- Correct obvious grammar mistakes.
- Ignore filler words like "uh", "umm", "ah" when appropriate.
- Do NOT summarize.
- Do NOT explain.
"""


def speech_to_text(audio):

    if audio is None:
        return ""

    # Save temporary wav file
    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp:

        temp.write(audio["bytes"])

        temp_path = temp.name

    uploaded_file = client.files.upload(
        file=temp_path
    )

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=[
            uploaded_file,
            TRANSCRIPTION_PROMPT
        ]

    )

    os.remove(temp_path)

    return response.text.strip()