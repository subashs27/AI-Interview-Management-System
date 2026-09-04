"""
Voice Recorder

Records audio from microphone using Streamlit.
"""

from streamlit_mic_recorder import mic_recorder


def record_voice():
    """
    Record audio from microphone.

    Returns:
        dict | None
    """

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="voice_recorder"
    )

    return audio