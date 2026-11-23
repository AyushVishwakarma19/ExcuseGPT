"""Favourites view for managing and copying saved excuses."""

import html
import streamlit as st

from frontend.styles import (
    format_approach_badge,
    get_approach_description,
    get_approach_meta,
    render_html,
    render_page_header,
    render_stat_kpi,
)


def render_favourites_view(persist_callback):
    """Render the redesigned sunlit Favourites management page."""

    render_page_header(
        badge="Curated Library",
        title="Saved Favourites",
        subtitle="Your personal collection of trusted explanations, organized by strategy and ready to copy anytime.",
    )

    saved_items = st.session_state.saved_excuses

    if not saved_items:
        render_html(
            """
            <div class="empty-canvas-box">
                <div class="empty-canvas-pill">Empty Collection</div>
                <div class="empty-canvas-title">No saved favourites yet</div>
                <div class="empty-canvas-desc">
                    Click <strong>Save to Favourites</strong> on any generated or refined response in the
                    <strong>Create</strong> or <strong>History</strong> views to keep it here.
                </div>
            </div>
            """
        )
        return

    # KPI Overview Strip
    total_saved = len(saved_items)
    refined_count = sum(1 for item in saved_items if "(Refined)" in item.get("title", ""))
    original_count = total_saved - refined_count

    kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
    with kpi1:
        render_stat_kpi("Total Saved", total_saved, "Persisted locally in SQLite")
    with kpi2:
        render_stat_kpi("Original Responses", original_count, "Primary AI strategies")
    with kpi3:
        render_stat_kpi("Refined Versions", refined_count, "Custom-tuned variations")

    st.markdown("<div style='height: 1.15rem;'></div>", unsafe_allow_html=True)

    # Search & Type Filter Toolbar
    with st.container(border=True):
        col_search, col_type = st.columns([3, 1], gap="medium")
        with col_search:
            search_kw = st.text_input(
                "Search favourites",
                placeholder="Search keywords in saved excuses, titles, or scenarios...",
                key="fav_search_box",
                label_visibility="collapsed",
            )
        with col_type:
            filter_type = st.selectbox(
                "Filter by Type",
                ["All Types", "Original Responses", "Refined Only"],
                key="fav_filter_type_select",
                label_visibility="collapsed",
            )

    # Filter items while preserving original list indices for removal
    filtered_items = []
    for idx, item in enumerate(saved_items):
        title = item.get("title", "")
        text = item.get("text", "")
        sit = item.get("situation", "")
        is_refined = "(Refined)" in title

        if filter_type == "Original Responses" and is_refined:
            continue
        if filter_type == "Refined Only" and not is_refined:
            continue

        if search_kw.strip():
            kw = search_kw.lower()
            if kw not in title.lower() and kw not in text.lower() and kw not in sit.lower():
                continue

        filtered_items.append((idx, item))

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    if not filtered_items:
        st.info("No favourites match your search or filter.")
        return

    st.caption(f"Showing {len(filtered_items)} of {total_saved} saved responses")

    # Responsive 2-column grid for saved favourites (stacks on mobile)
    grid_cols = st.columns(2, gap="medium")

    for grid_idx, (original_index, item) in enumerate(filtered_items):
        title = item.get("title", "Saved Excuse")
        text = item.get("text", "")
        situation = item.get("situation", "Context not specified")
        approach = item.get("approach", "direct_acknowledgement")
        is_refined = "(Refined)" in title

        meta = get_approach_meta(approach)
        badge_html = format_approach_badge(approach)
        approach_desc = get_approach_description(approach)

        safe_title = html.escape(str(title))
        safe_situation = html.escape(str(situation))
        safe_desc = html.escape(str(approach_desc))

        refined_tag_html = ""
        if is_refined:
            refined_tag_html = '<span class="refined-badge">Refined</span>'

        with grid_cols[grid_idx % 2]:
            with st.container(border=True):
                render_html(
                    f"""
                    <div class="response-top-accent" style="background: {meta['accent']};"></div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.45rem;">
                        {badge_html}
                        {refined_tag_html}
                    </div>
                    <h3 class="response-heading" style="margin-bottom: 0.3rem !important;">{safe_title}</h3>
                    <div class="strategy-caption" style="margin-bottom: 0.75rem;">
                        <strong>Strategy:</strong> {safe_desc}
                    </div>
                    <div class="situation-context-box">
                        <strong>Original Scenario:</strong><br/>{safe_situation}
                    </div>
                    """
                )

                st.code(text, language=None)

                if st.button(
                    "Remove from Favourites",
                    key=f"fav_remove_btn_{original_index}",
                    use_container_width=True,
                    help="Remove this response from your saved library.",
                ):
                    st.session_state.saved_excuses.pop(original_index)
                    persist_callback()
                    st.toast("Removed from favourites.")
                    st.rerun()

            st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)