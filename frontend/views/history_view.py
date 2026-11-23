"""History view for browsing past generations, refinements, and saved items."""

import html
import requests
import streamlit as st

from frontend.styles import (
    format_approach_badge,
    get_approach_description,
    get_approach_meta,
    render_html,
    render_page_header,
    render_stat_kpi,
)

REFINE_API_URL = "http://127.0.0.1:8000/refine"


def _format_generation_label(entry_id: str, fallback_index: int) -> str:
    """Format a display-only zero-padded generation number without altering stored IDs."""
    raw_id = str(entry_id).strip()
    if raw_id.isdigit():
        return f"{int(raw_id):02d}"
    return f"{fallback_index:02d}"


def render_history_view(persist_callback):
    """Render the redesigned sunlit Generation History page."""

    render_page_header(
        badge="Archive & Records",
        title="Generation History",
        subtitle="Browse previous scenarios, compare all three strategic angles, and refine or bookmark past responses.",
    )

    history = st.session_state.generation_history

    if not history:
        render_html(
            """
            <div class="empty-canvas-box">
                <div class="empty-canvas-pill">No Records Yet</div>
                <div class="empty-canvas-title">Your generation history is empty</div>
                <div class="empty-canvas-desc">
                    Switch to the <strong>Create</strong> tab to describe a situation and generate your first set of context-grounded responses.
                </div>
            </div>
            """
        )
        return

    # KPI Overview Strip
    total_generations = len(history)
    total_excuses = sum(len(entry.get("excuses", [])) for entry in history)
    categories = list({entry.get("preferences", {}).get("category", "General") for entry in history})

    kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
    with kpi1:
        render_stat_kpi("Total Generations", total_generations, "Saved locally in SQLite")
    with kpi2:
        render_stat_kpi("Responses Generated", total_excuses, "3 strategies per scenario")
    with kpi3:
        render_stat_kpi("Active Categories", len(categories), ", ".join(categories[:3]))

    st.markdown("<div style='height: 1.15rem;'></div>", unsafe_allow_html=True)

    # Search & Category Filter Bar
    with st.container(border=True):
        col_search, col_filter = st.columns([3, 1], gap="medium")
        with col_search:
            search_query = st.text_input(
                "Search history by keyword",
                placeholder="Search keywords in previous situations...",
                key="history_search_query",
                label_visibility="collapsed",
            )
        with col_filter:
            category_options = ["All Domains"] + sorted(list(set(
                entry.get("preferences", {}).get("category", "General") for entry in history
            )))
            selected_category = st.selectbox(
                "Filter Domain",
                category_options,
                key="history_category_filter",
                label_visibility="collapsed",
            )

    # Filter entries
    filtered_history = []
    for entry in history:
        sit_text = entry.get("situation", "")
        cat = entry.get("preferences", {}).get("category", "General")

        if selected_category != "All Domains" and cat != selected_category:
            continue
        if search_query.strip() and search_query.lower() not in sit_text.lower():
            continue
        filtered_history.append(entry)

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    if not filtered_history:
        st.info("No generations match your current search or domain filter.")
        return

    st.caption(f"Showing {len(filtered_history)} of {total_generations} generation records (newest first)")

    # Render each generation record
    for idx, entry in enumerate(filtered_history):
        entry_id = entry.get("id", str(idx + 1))
        display_num = _format_generation_label(entry_id, idx + 1)
        situation_text = entry.get("situation", "")
        prefs = entry.get("preferences", {})
        excuses = entry.get("excuses", [])

        cat = prefs.get("category", "General")
        tone = prefs.get("tone", "Casual")
        creat = prefs.get("creativity", "Medium")
        form = prefs.get("formality", "Balanced")
        length = prefs.get("length", "Medium")

        clean_sit = " ".join(situation_text.split())
        preview = clean_sit[:56] + ("..." if len(clean_sit) > 56 else "")
        expander_title = f"Generation {display_num} · {cat} — {preview}"

        with st.expander(expander_title, expanded=(idx == 0)):
            safe_cat = html.escape(str(cat))
            safe_tone = html.escape(str(tone))
            safe_creat = html.escape(str(creat))
            safe_form = html.escape(str(form))
            safe_length = html.escape(str(length))
            safe_situation = html.escape(situation_text)

            # Pastel metadata pills & grounding scenario callout
            render_html(
                f"""
                <div style="display: flex; gap: 0.45rem; flex-wrap: wrap; margin-bottom: 0.85rem;">
                    <span class="approach-pill" style="background: #FEF9C3; color: #713F12; border: 1px solid #FDE047;">Category: {safe_cat}</span>
                    <span class="approach-pill" style="background: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF;">Tone: {safe_tone}</span>
                    <span class="approach-pill" style="background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0;">Creativity: {safe_creat}</span>
                    <span class="approach-pill" style="background: #FFEDD5; color: #9A3412; border: 1px solid #FED7AA;">Formality: {safe_form}</span>
                    <span class="approach-pill" style="background: #F5F3EC; color: #3F3F46; border: 1px solid #E7E4DA;">Length: {safe_length}</span>
                </div>
                <div class="situation-context-box">
                    <strong>Grounding Scenario:</strong><br/>{safe_situation}
                </div>
                """
            )

            # 3-Column responsive layout for the 3 strategic variations (stacks on mobile)
            var_cols = st.columns(3, gap="medium")

            for excuse_index, excuse in enumerate(excuses):
                refinement_key = f"{entry_id}_{excuse_index}"
                approach_key = excuse.get("approach", "direct_acknowledgement")
                meta = get_approach_meta(approach_key)
                badge_html = format_approach_badge(approach_key)
                approach_desc = get_approach_description(approach_key)
                safe_title = html.escape(excuse.get("title", ""))
                safe_desc = html.escape(approach_desc)
                opt_num = excuse_index + 1

                with var_cols[excuse_index % 3]:
                    with st.container(border=True):
                        render_html(
                            f"""
                            <div class="response-top-accent" style="background: {meta['accent']};"></div>
                            <div class="response-meta-header">
                                <div class="response-title-group">
                                    <span class="response-num-tag">Option 0{opt_num}</span>
                                    {badge_html}
                                </div>
                            </div>
                            <h4 class="response-heading" style="margin-top: 0.45rem !important;">{safe_title}</h4>
                            <div class="strategy-caption"><strong>Strategy:</strong> {safe_desc}</div>
                            """
                        )

                        st.code(excuse["text"], language=None)

                        saved_item = {
                            "situation": situation_text,
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
                                key=f"hist_fav_{entry_id}_{excuse_index}",
                                use_container_width=True,
                            ):
                                st.session_state.saved_excuses.append(saved_item)
                                persist_callback()
                                st.toast("Saved to favourites.")
                                st.rerun()

                        # In-place refinement from history
                        with st.expander(f"Refine Option 0{opt_num}"):
                            with st.form(
                                key=f"hist_refine_form_{refinement_key}",
                                border=False,
                            ):
                                refine_input = st.text_area(
                                    "Refinement instruction",
                                    placeholder="e.g., Make it shorter, warmer, or more formal...",
                                    max_chars=500,
                                    height=100,
                                    key=f"hist_refine_in_{refinement_key}",
                                    label_visibility="collapsed",
                                )
                                refine_sub = st.form_submit_button(
                                    "Apply Refinement",
                                    type="primary",
                                    use_container_width=True,
                                )

                            if refine_sub:
                                if not refine_input.strip():
                                    st.warning("Please provide a refinement instruction.")
                                else:
                                    refinement_payload = {
                                        "situation": situation_text,
                                        "original_response": excuse["text"],
                                        "refinement_instruction": refine_input.strip(),
                                    }
                                    with st.spinner("Refining response..."):
                                        try:
                                            res = requests.post(
                                                REFINE_API_URL,
                                                json=refinement_payload,
                                                timeout=90,
                                            )
                                            if res.status_code == 200:
                                                refined_text = res.json().get(
                                                    "refined_text", ""
                                                ).strip()
                                                if refined_text:
                                                    st.session_state.refined_responses[
                                                        refinement_key
                                                    ] = refined_text
                                                    persist_callback()
                                                    st.toast("Refinement saved.")
                                                    st.rerun()
                                                else:
                                                    st.error("Empty refinement returned.")
                                            else:
                                                st.error("Refinement failed.")
                                        except Exception as e:
                                            st.error(f"Error: {e}")

                        # Display refinement if present
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
                                "situation": situation_text,
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
                                    key=f"hist_save_refined_{refinement_key}",
                                    use_container_width=True,
                                ):
                                    st.session_state.saved_excuses.append(refined_saved_item)
                                    persist_callback()
                                    st.toast("Refined response added to favourites.")
                                    st.rerun()