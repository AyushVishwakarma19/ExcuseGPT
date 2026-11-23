
import os
import streamlit as st


def get_backend_url() -> str:
    """Return the configured backend URL."""

    default_url = "http://127.0.0.1:8000"

    try:
        backend_url = st.secrets.get("BACKEND_URL", default_url)
    except (FileNotFoundError, KeyError):
        backend_url = os.getenv("BACKEND_URL", default_url)

    return backend_url.rstrip("/")


def use_session_storage() -> bool:
    """Use temporary per-session storage when enabled."""

    try:
        setting = st.secrets.get("SESSION_ONLY_STORAGE", "false")
    except (FileNotFoundError, KeyError):
        setting = os.getenv("SESSION_ONLY_STORAGE", "false")

    return str(setting).strip().lower() in {"true", "1", "yes"}
