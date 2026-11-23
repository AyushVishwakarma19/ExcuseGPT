"""ExcuseGPT — Main Streamlit Application Entrypoint.

Handles SQLite state persistence, sunlit editorial design injection,
custom horizontal top navigation (with zero sidebars), and multipage routing.
"""

import os
import sys

# Ensure project root is in sys.path for direct streamlit execution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import requests
import streamlit as st

from backend.services.storage_service import (
    load_app_state,
    save_app_state,
)
from frontend.config import get_backend_url, use_session_storage
from frontend.brand import render_full_logo_svg
from frontend.styles import inject_custom_css, render_html
from frontend.views.about_view import render_about_view
from frontend.views.create_view import render_create_view
from frontend.views.favourites_view import render_favourites_view
from frontend.views.history_view import render_history_view

# Browser favicon paths matching the ExcuseGPT sunlit logo mark
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FAVICON_PATH = os.path.join(ASSETS_DIR, "favicon.png")
LOGO_MARK_PATH = os.path.join(ASSETS_DIR, "logo_mark.svg")

PAGE_ICON = (
    FAVICON_PATH
    if os.path.exists(FAVICON_PATH)
    else (LOGO_MARK_PATH if os.path.exists(LOGO_MARK_PATH) else None)
)

# Page configuration — sidebar collapsed and completely hidden via CSS
st.set_page_config(
    page_title="ExcuseGPT — Context-Grounded AI Excuse Platform",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject global light editorial CSS design system
inject_custom_css()

# API configuration
# BACKEND_BASE_URL = "http://127.0.0.1:8000"
BACKEND_BASE_URL = get_backend_url()


# Load persistent application data from SQLite
if "app_state_loaded" not in st.session_state:
    if use_session_storage():
        st.session_state.generation_history = []
        st.session_state.saved_excuses = []
        st.session_state.refined_responses = {}
    else:
        saved_state = load_app_state()
        st.session_state.generation_history = saved_state["generation_history"]
        st.session_state.saved_excuses = saved_state["saved_excuses"]
        st.session_state.refined_responses = saved_state["refined_responses"]

    st.session_state.app_state_loaded = True


def persist_app_state():
    if not use_session_storage():
        save_app_state(
            generation_history=st.session_state.generation_history,
            saved_excuses=st.session_state.saved_excuses,
            refined_responses=st.session_state.refined_responses,
        )


def check_backend_health() -> bool:
    """Check whether the FastAPI backend is currently reachable."""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/", timeout=0.8)
        return response.status_code == 200
    except Exception:
        return False


# Define pages for native multipage URL routing (hidden default sidebar menu)
create_page = st.Page(
    lambda: render_create_view(persist_app_state),
    title="Create",
    url_path="create-excuses",
    default=True,
)
history_page = st.Page(
    lambda: render_history_view(persist_app_state),
    title="History",
    url_path="generation-history",
)
favourites_page = st.Page(
    lambda: render_favourites_view(persist_app_state),
    title="Favourites",
    url_path="saved-favourites",
)
about_page = st.Page(
    render_about_view,
    title="About",
    url_path="about-excusegpt",
)

current_page = st.navigation(
    [create_page, history_page, favourites_page, about_page],
    position="hidden",
)


def render_top_navigation(active_page):
    """Render a clean, responsive top navigation bar (4-column desktop, 2x2 mobile)."""
    brand_svg = render_full_logo_svg(height=36, dark_mode=False)
    is_online = check_backend_health()
    gen_count = len(st.session_state.generation_history)
    fav_count = len(st.session_state.saved_excuses)

    if is_online:
        status_html = (
            '<span class="top-nav-status-pill top-nav-status-online">'
            '<span class="status-dot-online"></span> AI Ready'
            '</span>'
        )
    else:
        status_html = (
            '<span class="top-nav-status-pill top-nav-status-offline" '
            'title="Start backend with: uvicorn backend.main:app --port 8000">'
            '<span class="status-dot-offline"></span> Backend Offline'
            '</span>'
        )

    # Top brand & live workspace status bar
    render_html(
        f"""
        <div class="top-nav-shell">
            <div class="top-nav-brand">
                {brand_svg}
            </div>
            <div class="top-nav-meta">
                <span class="top-nav-counts">
                    {gen_count} Generated &bull; {fav_count} Saved
                </span>
                {status_html}
            </div>
        </div>
        """
    )

    # Horizontal Navigation Tabs (4-column desktop, 2x2 grid below 640px via .st-key-top_nav_grid)
    nav_items = [
        ("Create", create_page, "nav_top_create"),
        (f"History ({gen_count})", history_page, "nav_top_history"),
        (f"Favourites ({fav_count})", favourites_page, "nav_top_favourites"),
        ("About", about_page, "nav_top_about"),
    ]

    with st.container(key="top_nav_grid"):
        nav_cols = st.columns(4, gap="small")
        for col, (label, target_page, btn_key) in zip(nav_cols, nav_items):
            is_active = active_page == target_page
            with col:
                if st.button(
                    label,
                    key=btn_key,
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                ):
                    if not is_active:
                        st.switch_page(target_page)

    st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)


render_top_navigation(current_page)
current_page.run()