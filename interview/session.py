"""
Streamlit Session Management

Stores a single InterviewState object inside Streamlit
session_state.
"""

import streamlit as st

from interview.interview_state import InterviewState


SESSION_KEY = "interview_state"


def initialize_session():
    """
    Initialize InterviewState once.
    """

    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = InterviewState()


def get_state() -> InterviewState:
    """
    Return the InterviewState object.
    """

    initialize_session()

    return st.session_state[SESSION_KEY]


def reset_interview():
    """
    Reset the interview session.
    """

    st.session_state[SESSION_KEY] = InterviewState()


def interview_started() -> bool:
    """
    Check whether interview has started.
    """

    state = get_state()

    return state.interview_started


def interview_finished() -> bool:
    """
    Check whether interview has finished.
    """

    state = get_state()

    return state.interview_finished


def start_interview():
    """
    Mark interview as started.
    """

    state = get_state()

    state.interview_started = True


def finish_interview():
    """
    Mark interview as finished.
    """

    state = get_state()

    state.interview_finished = True


def get_candidate():
    """
    Return candidate details.
    """

    return get_state().candidate


def set_candidate(candidate: dict):
    """
    Store candidate details.
    """

    get_state().candidate = candidate


def get_knowledge():
    """
    Return retrieved knowledge.
    """

    return get_state().knowledge


def set_knowledge(knowledge: list):
    """
    Store retrieved knowledge.
    """

    get_state().knowledge = knowledge