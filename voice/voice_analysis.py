"""
Voice Analysis

Extracts simple voice metrics from recorded audio.
"""

import tempfile
import os

import librosa


def analyze_voice(audio):

    if audio is None:

        return {}

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp:

        temp.write(audio["bytes"])

        path = temp.name

    y, sr = librosa.load(path, sr=None)

    duration = librosa.get_duration(y=y, sr=sr)

    rms = librosa.feature.rms(y=y)[0].mean()

    zero_crossings = librosa.feature.zero_crossing_rate(y)[0].mean()

    os.remove(path)

    return {

        "duration": round(duration, 2),

        "energy": round(float(rms), 4),

        "zero_crossing_rate": round(float(zero_crossings), 4)

    }


def speaking_rate(transcript, duration):

    if duration == 0:

        return 0

    words = len(transcript.split())

    wpm = (words / duration) * 60

    return round(wpm, 2)