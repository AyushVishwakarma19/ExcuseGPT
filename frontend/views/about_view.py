
"""About view presenting ExcuseGPT's purpose, principles, and architecture."""

import html

import streamlit as st

from frontend.brand import render_full_logo_svg, render_icon_svg
from frontend.styles import (
    APPROACH_METADATA,
    render_html,
    render_page_header,
)


def render_section_heading(icon_name: str, title: str, color: str):
    """Render a consistent section heading with an SVG icon."""
    icon = render_icon_svg(icon_name, size=19, color=color)
    safe_title = html.escape(title)

    render_html(
        f"""
        <div style="display:flex; align-items:center; gap:0.55rem;
                    margin-bottom:0.35rem;">
            {icon}
            <h3 style="margin:0; font-size:1.3rem; color:#18181B;">
                {safe_title}
            </h3>
        </div>
        """
    )


def render_about_view():
    """Render the About ExcuseGPT page."""

    # Product introduction
    render_page_header(
        badge="Get to Know the Product",
        title="About ExcuseGPT",
        subtitle=(
            "Because Every Situation Deserves an Exceptionally "
            "Creative Explanation."
        ),
    )

    full_logo_svg = render_full_logo_svg(height=42, dark_mode=False)

    render_html(
        f"""
        <div style="margin-bottom:1.1rem;">
            {full_logo_svg}
        </div>
        """
    )

    st.markdown(
        """
        **ExcuseGPT** is an AI-powered explanation generation and
        refinement platform designed to make everyday communication
        easier.

        Whether you're navigating a professional, academic, social,
        or personal situation, ExcuseGPT helps you express what
        happened through three distinct, natural-sounding responses.

        The goal is simple: communicate more thoughtfully without
        changing the facts.
        """
    )

    st.markdown("<div style='height:1.1rem;'></div>",
                unsafe_allow_html=True)

    # Core philosophy
    render_section_heading(
        "shield",
        "Our Core Philosophy",
        "#166534",
    )

    st.markdown(
        """
        ExcuseGPT follows one central principle: **creativity should
        improve how something is expressed, never rewrite what
        actually happened.**
        """
    )

    with st.container(border=True):
        render_html(
            """
            <div style="background:#FEF9C3;
                        border-left:4px solid #EAB308;
                        border-radius:0 10px 10px 0;
                        padding:1rem 1.2rem;
                        margin-bottom:1rem;">
                <div style="font-size:1.12rem;
                            font-weight:800;
                            color:#18181B;">
                    "Creativity adapts expression, not reality."
                </div>
                <div style="color:#52525B;
                            font-size:0.88rem;
                            margin-top:0.4rem;
                            line-height:1.55;">
                    A better explanation does not need a fabricated
                    emergency, fictional event, or unsupported claim.
                </div>
            </div>
            """
        )

        st.markdown(
            """
            - **Fact preservation:** Responses are designed to retain
              the circumstances supplied by the user.
            - **Grounding validation:** Automated checks identify
              common patterns of unsupported actions, commitments,
              locations, and time references.
            - **Natural communication:** Creativity focuses on
              wording, tone, emotional expression, and clarity.
            - **User responsibility:** Generated responses should
              be reviewed before being used or sent.
            """
        )

    st.markdown("<div style='height:1.1rem;'></div>",
                unsafe_allow_html=True)

    # How the product works
    render_section_heading(
        "workflow",
        "How ExcuseGPT Works",
        "#6B21A8",
    )

    st.markdown(
        """
        The generation process combines your original context,
        customization preferences, AI-generated language, and
        structured validation.
        """
    )

    workflow_steps = [
        (
            "01",
            "Describe the Situation",
            "Provide the actual circumstances and relevant details.",
        ),
        (
            "02",
            "Choose Your Preferences",
            "Select the communication context, tone, and formality.",
        ),
        (
            "03",
            "Generate Three Responses",
            "Receive three distinct explanations with different "
            "communication approaches.",
        ),
        (
            "04",
            "Refine and Save",
            "Copy, refine, or favourite responses and revisit "
            "previous generations through History.",
        ),
    ]

    for number, title, description in workflow_steps:
        with st.container(border=True):
            render_html(
                f"""
                <div style="display:flex; align-items:flex-start;
                            gap:0.85rem;">
                    <div style="flex-shrink:0;
                                background:#FEF9C3;
                                border:1px solid #FDE047;
                                border-radius:9px;
                                padding:0.35rem 0.6rem;
                                font-size:0.75rem;
                                font-weight:800;
                                color:#854D0E;">
                        {html.escape(number)}
                    </div>
                    <div>
                        <div style="font-weight:750;
                                    font-size:0.96rem;
                                    color:#18181B;
                                    margin-bottom:0.25rem;">
                            {html.escape(title)}
                        </div>
                        <div style="font-size:0.85rem;
                                    line-height:1.5;
                                    color:#52525B;">
                            {html.escape(description)}
                        </div>
                    </div>
                </div>
                """
            )

    st.markdown("<div style='height:1.1rem;'></div>",
                unsafe_allow_html=True)

    # Response strategies
    render_section_heading(
        "cpu",
        "Five Response Strategies",
        "#6B21A8",
    )

    st.markdown(
        """
        Each generation provides three distinct responses drawn
        from different communication approaches. The available
        strategies help vary the way a situation is expressed.
        """
    )

    for key, data in APPROACH_METADATA.items():
        with st.container(border=True):
            col_left, col_right = st.columns([1, 3])

            with col_left:
                safe_label = html.escape(data["label"])
                render_html(
                    f"""
                    <span class="approach-pill"
                          style="background-color:{data['badge_bg']};
                                 color:{data['badge_color']};
                                 border:1px solid {data['badge_border']};
                                 font-size:0.82rem;
                                 padding:0.35rem 0.75rem;">
                        {safe_label}
                    </span>
                    """
                )

            with col_right:
                st.markdown(
                    f"**Approach:** {data['description']}"
                )

    st.markdown("<div style='height:1.1rem;'></div>",
                unsafe_allow_html=True)

    # Technology stack
    render_section_heading(
        "terminal",
        "Technology & Architecture",
        "#9A3412",
    )

    st.markdown(
        """
        ExcuseGPT uses a Python-based frontend and backend,
        with an external AI service for generation and refinement.
        """
    )

    # First row: Frontend and Backend & AI
    with st.container(key="tech_frontend_row"):
        col_frontend, col_backend = st.columns(
            2,
            gap="small",
        )

        with col_frontend:
            with st.container(border=True):
                st.markdown("#### Frontend")
                st.markdown(
                    """
                    - **Framework:** Streamlit
                    - **Language:** Python 3.12
                    - **Styling:** Custom HTML and CSS
                    - **Navigation:** Create, History, Favourites, About
                    - **Interactions:** Generation, copying, refinement,
                      and favourite management
                    """
                )

        with col_backend:
            with st.container(border=True):
                st.markdown("#### Backend & AI")
                st.markdown(
                    """
                    - **API Framework:** FastAPI
                    - **Server:** Uvicorn
                    - **AI Integration:** Google Gemini Developer API
                    - **Data Validation:** Pydantic schemas
                    - **Grounding:** Custom grounding validator
                    - **Input Validation:** Enforces required fields and valid values.
                    """
                )

    # Second row: Storage and Quality
    with st.container(key="tech_storage_row"):
        col_storage, col_quality = st.columns(
            2,
            gap="small",
        )

        with col_storage:
            with st.container(border=True):
                st.markdown("#### Storage & Persistence")
                st.markdown(
                    """
                    - **Database:** SQLite
                    - **Integration:** Python `sqlite3`
                    - **Stored Data:** Generation history and
                      saved favourites
                    - **Persistence:** Application records remain
                      available across restarts and reloads
                    """
                )

        with col_quality:
            with st.container(border=True):
                st.markdown("#### Quality & Testing")
                st.markdown(
                    """
                    - **Automated Tests:** 42 passing tests
                    - **API Testing:** Generation and refinement
                    - **Validation Testing:** Grounding and schemas
                    - **Storage Testing:** Database persistence
                    - **Reliability:** Input and error-handling checks
                    """
                )

    st.markdown("<div style='height:1.1rem;'></div>",
                unsafe_allow_html=True)

    # Data and privacy transparency
    render_section_heading(
        "lock",
        "Data & Privacy Transparency",
        "#166534",
    )

    with st.container(border=True):
        st.markdown(
            """
            ExcuseGPT uses local storage for application records
            and an external AI service to generate and refine
            responses.

            - **Local persistence:** Generation history and
              favourites are stored in the application's SQLite
              database on the machine running the application.
            - **External AI processing:** Situation details and
              relevant generation or refinement parameters are
              sent to Google's Gemini Developer API when those
              operations are requested.
            - **Service limitations:** API quotas, rate limits,
              and availability are subject to Google's service
              terms and may change.
            """
        )

        render_html(
            """
            <div style="background:#F5F3EC;
                        border:1px solid #E7E4DA;
                        border-radius:10px;
                        padding:0.8rem 1rem;
                        margin-bottom:0.35rem;
                        font-size:0.84rem;
                        line-height:1.55;
                        color:#52525B;">
                <strong style="color:#18181B;">
                    A helpful reminder
                </strong><br>
                Avoid entering passwords, sensitive personal
                information, or confidential details into the
                application.
            </div>
            """
        )

    st.markdown("<div style='height:1.2rem;'></div>",
                unsafe_allow_html=True)

    st.caption(
        "ExcuseGPT • Context-Grounded AI Studio • "
        "Built with Python, Streamlit, FastAPI & Gemini"
    )
