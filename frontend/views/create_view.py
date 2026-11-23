"""Create view for generating and refining context-grounded excuses."""

import html
import requests
import streamlit as st

from frontend.brand import render_icon_svg
from frontend.styles import (
    format_approach_badge,
    get_approach_description,
    get_approach_meta,
    render_html,
)

API_URL = "http://127.0.0.1:8000/generate"
REFINE_API_URL = "http://127.0.0.1:8000/refine"


def render_create_view(persist_callback):
    """Render the redesigned sunlit Create workspace for generating and refining excuses."""

    shield_svg = render_icon_svg("shield", size=15, color="#166534")

    # Welcoming Editorial Hero Header
    render_html(
        f"""
        <div class="create-hero">
            <div>
                <div class="page-header-badge">Context-Grounded AI Studio</div>
                <h1 class="create-hero-title">Craft the right explanation, honestly.</h1>
                <p class="create-hero-desc">
                    Describe what actually happened and choose your delivery preferences.
                    ExcuseGPT generates three distinct, natural responses rooted strictly in your facts.
                </p>
            </div>
            <div class="grounding-chip">
                {shield_svg}
                <span><strong>Fact-Preserving:</strong> Adapts expression, never reality</span>
            </div>
        </div>
        """
    )

    # =========================================================================
    # COMPOSER WORKSPACE: Situation Input + Preferences + Primary Action
    # =========================================================================
    with st.container(border=True):
        render_html(
            """
            <div class="composer-section-label">
                <span class="composer-step-pill">01 &bull; Situation</span>
            </div>
            <div class="composer-title">What actually happened?</div>
            <div class="composer-hint">
                Share genuine details, timing conflicts, or honest oversights. All three responses will preserve these facts.
            </div>
            """
        )

        situation = st.text_area(
            "What actually happened?",
            placeholder="e.g., I misjudged morning traffic during heavy rain and arrived 25 minutes late to our project kickoff meeting...",
            max_chars=3000,
            height=130,
            key="situation_text_area",
            label_visibility="collapsed",
            help="Describe authentic facts. ExcuseGPT preserves these circumstances across all 3 strategic options.",
        )

        render_html(
            """
            <div class="composer-divider"></div>
            <div class="composer-section-label">
                <span class="composer-step-pill">02 &bull; Preferences</span>
            </div>
            <div class="composer-hint" style="margin-bottom: 0.6rem;">
                Shape the context, emotional tone, and structure of your three responses.
            </div>
            """
        )

        # Clean 5-column preference bar (stacks smoothly on narrow screens)
        col_cat, col_tone, col_creat, col_form, col_len = st.columns(5, gap="small")
        with col_cat:
            category = st.selectbox(
                "Category",
                ["Academic", "Work", "Personal", "Social", "General"],
                key="pref_category",
                help="Contextual domain for the situation.",
            )
        with col_tone:
            tone = st.selectbox(
                "Tone",
                ["Funny", "Professional", "Polite", "Casual", "Apologetic"],
                key="pref_tone",
                help="Emotional posture and interpersonal delivery.",
            )
        with col_creat:
            creativity = st.selectbox(
                "Creativity",
                ["Low", "Medium", "High"],
                index=1,
                key="pref_creativity",
                help="Phrasing flexibility without altering facts.",
            )
        with col_form:
            formality = st.selectbox(
                "Formality",
                ["Casual", "Balanced", "Formal"],
                key="pref_formality",
                help="Vocabulary and diction level.",
            )
        with col_len:
            length = st.selectbox(
                "Length",
                ["Short", "Medium", "Long"],
                index=1,
                key="pref_length",
                help="Target response length.",
            )

        st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)

        # Action row: helper caption on left, distinctive Lemon Yellow CTA on right
        col_note, col_cta = st.columns([3, 2], gap="medium")
        with col_note:
            render_html(
                """
                <div style="font-size: 0.82rem; color: #71717A; padding-top: 0.55rem;">
                    Generates <strong>3 distinct strategic approaches</strong> tailored to your exact scenario.
                </div>
                """
            )
        with col_cta:
            generate_clicked = st.button(
                "Generate 3 Grounded Responses",
                type="primary",
                use_container_width=True,
                key="btn_generate_main",
            )

    # =========================================================================
    # GENERATION EXECUTION (Preserves exact API payload & session state)
    # =========================================================================
    if generate_clicked:
        if not situation.strip():
            st.warning("Please describe your situation first before generating.")
        else:
            payload = {
                "situation": situation.strip(),
                "category": category,
                "tone": tone,
                "creativity": creativity,
                "formality": formality,
                "length": length,
            }

            with st.spinner("Crafting 3 context-grounded responses..."):
                try:
                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=90,
                    )

                    if response.status_code == 200:
                        result = response.json()
                        generation_id = str(
                            len(st.session_state.generation_history) + 1
                        )

                        new_entry = {
                            "id": generation_id,
                            "situation": situation.strip(),
                            "preferences": payload.copy(),
                            "excuses": result["excuses"],
                        }

                        st.session_state.generation_history.insert(0, new_entry)
                        st.session_state.current_generation_id = generation_id
                        persist_callback()
                        st.toast("3 grounded responses ready.")
                        st.rerun()

                    elif response.status_code == 503:
                        st.warning(
                            "The AI service is temporarily unavailable due to upstream rate limits. "
                            "Please try again in a few moments."
                        )
                    else:
                        try:
                            error_detail = response.json().get(
                                "detail",
                                "Unable to generate excuses.",
                            )
                        except ValueError:
                            error_detail = "Unable to generate excuses."
                        st.error(f"Generation error: {error_detail}")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to the backend server. "
                        "Please ensure the FastAPI service is running at http://127.0.0.1:8000."
                    )
                except requests.exceptions.Timeout:
                    st.error("The request timed out. Please try again.")
                except requests.exceptions.RequestException:
                    st.error("A network error occurred while reaching the backend.")

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # GENERATED RESPONSES SECTION (Central Product Experience)
    # =========================================================================
    if not st.session_state.generation_history:
        render_html(
            """
            <div class="empty-canvas-box">
                <div class="empty-canvas-pill">Ready When You Are</div>
                <div class="empty-canvas-title">Your three tailored responses will appear here</div>
                <div class="empty-canvas-desc">
                    Enter your situation above and click <strong>Generate 3 Grounded Responses</strong>.
                    Every generation explores three distinct communication angles without inventing fake emergencies.
                </div>
                <div class="empty-strategy-preview">
                    <div class="empty-strategy-item" style="border-top: 3px solid #A855F7;">
                        <div class="empty-strategy-num" style="color: #6B21A8;">Approach 01</div>
                        <div class="empty-strategy-name">Direct Acknowledgement</div>
                        <div class="empty-strategy-text">Clear, candid ownership without evasion or deflection.</div>
                    </div>
                    <div class="empty-strategy-item" style="border-top: 3px solid #22C55E;">
                        <div class="empty-strategy-num" style="color: #166534;">Approach 02</div>
                        <div class="empty-strategy-name">Alternative Framing</div>
                        <div class="empty-strategy-text">Constructive context around genuine competing priorities.</div>
                    </div>
                    <div class="empty-strategy-item" style="border-top: 3px solid #F97316;">
                        <div class="empty-strategy-num" style="color: #9A3412;">Approach 03</div>
                        <div class="empty-strategy-name">Accountability & Recovery</div>
                        <div class="empty-strategy-text">Takes responsibility and focuses on practical next steps.</div>
                    </div>
                </div>
            </div>
            """
        )
        return

    latest_entry = st.session_state.generation_history[0]
    safe_situation = html.escape(latest_entry.get("situation", ""))
    prefs = latest_entry.get("preferences", {})

    render_html(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.65rem;">
            <div>
                <h2 style="margin: 0; font-size: 1.4rem;">Generated Responses</h2>
                <div style="font-size: 0.84rem; color: #71717A;">
                    Three distinct strategic options &bull; {html.escape(str(prefs.get('category', 'General')))} &bull; {html.escape(str(prefs.get('tone', 'Balanced')))}
                </div>
            </div>
            <span class="page-header-badge" style="margin-bottom: 0;">3 Distinct Strategies</span>
        </div>
        <div class="situation-context-box">
            <strong>Grounding Scenario:</strong> {safe_situation}
        </div>
        """
    )

    # Render the 3 generated responses in a responsive 3-column showcase grid (stacks on mobile)
    response_cols = st.columns(3, gap="medium")

    for excuse_index, excuse in enumerate(latest_entry["excuses"]):
        refinement_key = f"{latest_entry['id']}_{excuse_index}"
        approach_key = excuse.get("approach", "direct_acknowledgement")
        meta = get_approach_meta(approach_key)
        badge_html = format_approach_badge(approach_key)
        approach_desc = get_approach_description(approach_key)
        safe_title = html.escape(excuse.get("title", ""))
        safe_desc = html.escape(approach_desc)
        opt_num = excuse_index + 1

        col_target = response_cols[excuse_index % 3]
        with col_target:
            with st.container(border=True):
                # Pastel strategy top accent bar
                render_html(
                    f"""
                    <div class="response-top-accent" style="background: {meta['accent']};"></div>
                    <div class="response-meta-header">
                        <div class="response-title-group">
                            <span class="response-num-tag">Option 0{opt_num}</span>
                            {badge_html}
                        </div>
                    </div>
                    <h3 class="response-heading" style="margin-top: 0.45rem !important;">{safe_title}</h3>
                    <div class="strategy-caption">
                        <strong>Strategy:</strong> {safe_desc}
                    </div>
                    """
                )

                # Formatted response card body with built-in accessible copy control
                st.code(excuse["text"], language=None)

                # Save / Favourites action
                saved_item = {
                    "situation": latest_entry["situation"],
                    "title": excuse["title"],
                    "text": excuse["text"],
                    "approach": excuse["approach"],
                }
                is_saved = saved_item in st.session_state.saved_excuses

                if is_saved:
                    render_html(
                        """
                        <div style="margin-bottom: 0.65rem;">
                            <span class="saved-status-pill">&#9733; Saved to Favourites</span>
                        </div>
                        """
                    )
                else:
                    if st.button(
                        "Save to Favourites",
                        key=f"create_fav_{latest_entry['id']}_{excuse_index}",
                        use_container_width=True,
                    ):
                        st.session_state.saved_excuses.append(saved_item)
                        persist_callback()
                        st.toast("Saved to favourites.")
                        st.rerun()

                # Integrated Refinement Controls
                with st.expander(f"Refine Option 0{opt_num}"):
                    with st.form(
                        key=f"create_refine_form_{refinement_key}",
                        border=False,
                    ):
                        refinement_instruction = st.text_area(
                            "Refinement instruction",
                            placeholder=(
                                "e.g., Make it shorter, warmer, or more direct..."
                            ),
                            max_chars=500,
                            height=100,
                            key=f"refine_in_{refinement_key}",
                            label_visibility="collapsed",
                        )
                        refine_submitted = st.form_submit_button(
                            "Apply Refinement",
                            type="primary",
                            use_container_width=True,
                        )

                    if refine_submitted:
                        if not refinement_instruction.strip():
                            st.warning("Please enter a refinement instruction.")
                        else:
                            refinement_payload = {
                                "situation": latest_entry["situation"],
                                "original_response": excuse["text"],
                                "refinement_instruction": refinement_instruction.strip(),
                            }

                            with st.spinner("Refining response..."):
                                try:
                                    refine_res = requests.post(
                                        REFINE_API_URL,
                                        json=refinement_payload,
                                        timeout=90,
                                    )

                                    if refine_res.status_code == 200:
                                        refined_text = refine_res.json().get(
                                            "refined_text", ""
                                        ).strip()

                                        if refined_text:
                                            st.session_state.refined_responses[
                                                refinement_key
                                            ] = refined_text
                                            persist_callback()
                                            st.toast("Response refined.")
                                            st.rerun()
                                        else:
                                            st.error("The AI returned an empty response.")
                                    elif refine_res.status_code == 503:
                                        st.warning("The AI service is temporarily unavailable.")
                                    else:
                                        err = refine_res.json().get(
                                            "detail", "Unable to refine this response."
                                        )
                                        st.error(f"Refinement error: {err}")
                                except requests.exceptions.ConnectionError:
                                    st.error("Cannot connect to backend.")
                                except requests.exceptions.Timeout:
                                    st.error("Refinement request timed out.")
                                except requests.exceptions.RequestException:
                                    st.error("A network error occurred.")

                # Display Refined Variation if present
                if refinement_key in st.session_state.refined_responses:
                    refined_text = st.session_state.refined_responses[refinement_key]
                    render_html(
                        """
                        <div class="refined-container">
                            <span class="refined-badge">Refined Version</span>
                        </div>
                        """
                    )
                    st.code(refined_text, language=None)

                    refined_saved_item = {
                        "situation": latest_entry["situation"],
                        "title": f"{excuse['title']} (Refined)",
                        "text": refined_text,
                        "approach": excuse["approach"],
                    }

                    if refined_saved_item in st.session_state.saved_excuses:
                        render_html(
                            """
                            <div style="margin-top: 0.35rem;">
                                <span class="saved-status-pill">&#9733; Refined Version Saved</span>
                            </div>
                            """
                        )
                    else:
                        if st.button(
                            "Save Refined to Favourites",
                            key=f"save_refined_{refinement_key}",
                            use_container_width=True,
                        ):
                            st.session_state.saved_excuses.append(refined_saved_item)
                            persist_callback()
                            st.toast("Refined response added to favourites.")
                            st.rerun()