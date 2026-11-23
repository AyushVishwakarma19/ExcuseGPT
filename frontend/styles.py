"""ExcuseGPT Light Editorial Design System & Visual Presentation Layer.

Implements a bright, warm, sunlit SaaS aesthetic:
- Warm Alabaster & Pure White surfaces (#FAF9F5, #FFFFFF, #F5F3EC)
- Distinctive Lemon Yellow primary accent (#FACC15) & Pale Buttery Yellow (#FEF9C3)
- Pastel strategy differentiation: Lavender, Sage Mint, Pastel Peach, Butter Yellow, Blush Rose
- Deep Charcoal typography (#18181B) for effortless readability
- Zero sidebars with a clean horizontal top navigation bar (and 2x2 grid on mobile)
- Lightweight, accessible CSS micro-interactions and floating ambient shapes
"""

import html
import streamlit as st

# Approach metadata mapping: labels, pastel palette tokens, and strategy descriptions
APPROACH_METADATA = {
    "direct_acknowledgement": {
        "label": "Direct Acknowledgement",
        "description": "Honestly states what occurred without deflection, manufacturing excuses, or evasion.",
        "badge_bg": "#F3E8FF",
        "badge_color": "#6B21A8",
        "badge_border": "#E9D5FF",
        "accent": "#A855F7",
        "card_tint": "#FBF7FF",
    },
    "alternative_framing": {
        "label": "Alternative Framing",
        "description": "Frames the situation around genuine competing priorities while remaining factual.",
        "badge_bg": "#DCFCE7",
        "badge_color": "#166534",
        "badge_border": "#BBF7D0",
        "accent": "#22C55E",
        "card_tint": "#F6FEF9",
    },
    "accountability_recovery": {
        "label": "Accountability & Recovery",
        "description": "Takes ownership of the outcome and emphasizes practical resolution.",
        "badge_bg": "#FFEDD5",
        "badge_color": "#9A3412",
        "badge_border": "#FED7AA",
        "accent": "#F97316",
        "card_tint": "#FFF9F3",
    },
    "light_humour": {
        "label": "Light Humour",
        "description": "De-escalates tension with gentle, relatable, situation-appropriate wit.",
        "badge_bg": "#FEF9C3",
        "badge_color": "#854D0E",
        "badge_border": "#FDE047",
        "accent": "#EAB308",
        "card_tint": "#FFFDF2",
    },
    "emotional_expression": {
        "label": "Emotional Expression",
        "description": "Conveys sincere regret, human vulnerability, and thoughtful consideration.",
        "badge_bg": "#FCE7F3",
        "badge_color": "#9D174D",
        "badge_border": "#FBCFE8",
        "accent": "#EC4899",
        "card_tint": "#FFF7FB",
    },
}

CUSTOM_CSS = """
<style>
/* =========================================================================
   ExcuseGPT Sunlit Editorial SaaS Design System (v3.2 Mobile Nav Grid Fix)
   Canvas: Warm Ivory (#FAF9F5) | Surfaces: Pure White (#FFFFFF)
   Primary Accent: Lemon Yellow (#FACC15) & Butter (#FEF9C3)
   Supporting Pastels: Lavender (#F3E8FF), Peach (#FFEDD5), Mint (#DCFCE7)
   Ink: Deep Charcoal (#18181B)
   ========================================================================= */

:root {
    --bg-canvas: #FAF9F5;
    --bg-surface: #FFFFFF;
    --bg-ivory-subtle: #F5F3EC;
    --border-hairline: #E7E4DA;
    --border-strong: #D6D2C4;
    --accent-lemon: #FACC15;
    --accent-lemon-hover: #EAB308;
    --accent-butter: #FEF9C3;
    --accent-lavender: #F3E8FF;
    --accent-peach: #FFEDD5;
    --accent-mint: #DCFCE7;
    --ink-primary: #18181B;
    --ink-secondary: #52525B;
    --ink-muted: #71717A;
}

/* Strictly remove left & right sidebars */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
}

/* Safely hide Streamlit Deploy button & toolbar menu overlay without breaking navigation */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    pointer-events: none !important;
}

[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
.stDeployButton,
#MainMenu,
[data-testid="stMainMenu"],
[data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

/* App Canvas Background & Overflow Safeguard */
html, body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #FAF9F5 !important;
    color: #18181B !important;
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

/* Centered, balanced editorial container */
.block-container {
    padding-top: 1.15rem !important;
    padding-bottom: 4rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1220px !important;
}

/* =========================================================================
   Subtle Ambient Floating Background Elements (Lightweight CSS Only)
   ========================================================================= */
.ambient-canvas {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.ambient-orb {
    position: absolute;
    border-radius: 50%;
    opacity: 0.55;
    will-change: transform;
}

.ambient-orb-lemon {
    width: 340px;
    height: 340px;
    top: -90px;
    right: 6%;
    background: radial-gradient(circle, rgba(254, 249, 195, 0.9) 0%, rgba(254, 249, 195, 0) 72%);
    animation: floatSlowA 18s ease-in-out infinite alternate;
}

.ambient-orb-lavender {
    width: 380px;
    height: 380px;
    top: 38%;
    left: -110px;
    background: radial-gradient(circle, rgba(243, 232, 255, 0.85) 0%, rgba(243, 232, 255, 0) 72%);
    animation: floatSlowB 22s ease-in-out infinite alternate;
}

.ambient-orb-peach {
    width: 320px;
    height: 320px;
    bottom: -80px;
    right: 14%;
    background: radial-gradient(circle, rgba(255, 237, 213, 0.85) 0%, rgba(255, 237, 213, 0) 72%);
    animation: floatSlowA 20s ease-in-out infinite alternate-reverse;
}

@keyframes floatSlowA {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    100% { transform: translate3d(-18px, 22px, 0) scale(1.04); }
}

@keyframes floatSlowB {
    0% { transform: translate3d(0, 0, 0) scale(1); }
    100% { transform: translate3d(20px, -18px, 0) scale(1.03); }
}

@keyframes cardFadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    .ambient-orb,
    .page-header-container,
    .stat-kpi-card,
    .response-card-header,
    [data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        animation: none !important;
        transition: none !important;
    }
}

/* =========================================================================
   Typography System
   ========================================================================= */
h1, h2, h3, h4, h5, h6 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif !important;
    color: #18181B !important;
    letter-spacing: -0.025em !important;
    font-weight: 700 !important;
}

p, span, label, div, li {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
    color: #18181B;
}

/* =========================================================================
   Horizontal Top Navigation Bar
   ========================================================================= */
.top-nav-shell {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.65rem;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid #E7E4DA;
    border-radius: 16px;
    padding: 0.65rem 1.15rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 20px rgba(24, 24, 27, 0.04);
}

.top-nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
}

.top-nav-meta {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-wrap: wrap;
}

.top-nav-counts {
    font-size: 0.78rem;
    color: #71717A;
    font-weight: 600;
    white-space: nowrap;
}

.top-nav-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.28rem 0.72rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    white-space: nowrap;
}

.top-nav-status-online {
    background: #DCFCE7;
    color: #166534;
    border: 1px solid #BBF7D0;
}

.top-nav-status-offline {
    background: #FFEDD5;
    color: #9A3412;
    border: 1px solid #FED7AA;
}

.status-dot-online {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #16A34A;
    display: inline-block;
    flex-shrink: 0;
}

.status-dot-offline {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #EA580C;
    display: inline-block;
    flex-shrink: 0;
}

/* Keep dedicated top_nav_grid container transparent so desktop 4-column layout is unchanged */
.st-key-top_nav_grid,
[class*="st-key-top_nav_grid"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    animation: none !important;
}

/* =========================================================================
   Unified Page Header & Editorial Hero
   ========================================================================= */
.page-header-container {
    margin-bottom: 1.35rem;
    animation: cardFadeIn 0.35s ease-out;
}

.page-header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #713F12;
    background: #FEF9C3;
    border: 1px solid #FDE047;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    margin-bottom: 0.55rem;
}

.page-header-title {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #18181B !important;
    letter-spacing: -0.035em !important;
    margin: 0 0 0.35rem 0 !important;
    line-height: 1.18 !important;
}

.page-header-subtitle {
    font-size: 1rem;
    color: #52525B;
    line-height: 1.55;
    margin: 0;
    max-width: 760px;
}

/* Create Hero Banner */
.create-hero {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.35rem;
    animation: cardFadeIn 0.35s ease-out;
}

.create-hero-title {
    font-size: 2.05rem !important;
    font-weight: 800 !important;
    color: #18181B !important;
    letter-spacing: -0.035em !important;
    line-height: 1.15 !important;
    margin: 0.35rem 0 0.35rem 0 !important;
}

.create-hero-desc {
    font-size: 0.975rem;
    color: #52525B;
    line-height: 1.55;
    margin: 0;
    max-width: 680px;
}

.grounding-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: #FFFFFF;
    border: 1px solid #E7E4DA;
    border-radius: 12px;
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
    color: #52525B;
    box-shadow: 0 2px 8px rgba(24, 24, 27, 0.03);
}

.grounding-chip strong {
    color: #18181B;
    font-weight: 700;
}

/* =========================================================================
   Card & Container Surfaces
   ========================================================================= */
[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:not(.st-key-top_nav_grid) {
    background: #FFFFFF !important;
    border: 1px solid #E7E4DA !important;
    border-radius: 16px !important;
    padding: 1.35rem !important;
    box-shadow: 0 6px 24px rgba(24, 24, 27, 0.035) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    animation: cardFadeIn 0.35s ease-out;
}

[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:not(.st-key-top_nav_grid):hover {
    border-color: #D6D2C4 !important;
    box-shadow: 0 8px 28px rgba(24, 24, 27, 0.055) !important;
}

/* Section Headers inside Composer */
.composer-section-label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.45rem;
}

.composer-step-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #713F12;
    background: #FEF9C3;
    border: 1px solid #FDE047;
    padding: 0.18rem 0.6rem;
    border-radius: 6px;
}

.composer-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #18181B;
    margin: 0.25rem 0 0.2rem 0;
}

.composer-hint {
    font-size: 0.84rem;
    color: #71717A;
    margin-bottom: 0.75rem;
}

.composer-divider {
    height: 1px;
    background: #F0EDE4;
    margin: 1rem 0 0.9rem 0;
}

/* =========================================================================
   Generated Response Cards & Accessible Copy Control
   ========================================================================= */
.response-top-accent {
    height: 4px;
    border-radius: 9999px;
    margin-bottom: 0.95rem;
}

.response-meta-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}

.response-title-group {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    flex-wrap: wrap;
}

.response-num-tag {
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.22rem 0.6rem;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: #F5F3EC;
    color: #52525B;
    border: 1px solid #E7E4DA;
}

.response-heading {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #18181B !important;
    margin: 0 !important;
    letter-spacing: -0.015em !important;
    line-height: 1.3 !important;
}

.approach-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.73rem;
    font-weight: 700;
    padding: 0.24rem 0.7rem;
    border-radius: 9999px;
    letter-spacing: 0.015em;
}

.strategy-caption {
    font-size: 0.84rem;
    color: #52525B;
    line-height: 1.5;
    margin: 0.25rem 0 0.85rem 0;
}

.strategy-caption strong {
    color: #18181B;
    font-weight: 600;
}

/* Editorial Response Text Container with Permanently Visible Copy Button */
div[data-testid="stCode"] {
    position: relative !important;
    background-color: #FAF9F5 !important;
    border: 1px solid #E7E4DA !important;
    border-radius: 12px !important;
    padding: 0.6rem 0.8rem !important;
    box-shadow: inset 0 1px 3px rgba(24, 24, 27, 0.03) !important;
    margin-bottom: 0.75rem !important;
}

div[data-testid="stCode"] pre {
    background: transparent !important;
    padding: 0.45rem 2.5rem 0.45rem 0.35rem !important;
    margin: 0 !important;
}

div[data-testid="stCode"] code {
    color: #18181B !important;
    font-size: 1.02rem !important;
    line-height: 1.72 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: -0.008em !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}

/* Make native copy button always visible, tactile, and accessible on touchscreens */
div[data-testid="stCode"] button,
div[data-testid="stCode"] button[title="Copy to clipboard"],
div[data-testid="stCode"] [data-testid="stCodeCopyButton"] {
    opacity: 1 !important;
    visibility: visible !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 34px !important;
    min-height: 34px !important;
    background: #FFFFFF !important;
    border: 1px solid #D6D2C4 !important;
    border-radius: 8px !important;
    color: #18181B !important;
    box-shadow: 0 2px 6px rgba(24, 24, 27, 0.06) !important;
    transition: all 0.18s ease !important;
}

div[data-testid="stCode"] button:hover,
div[data-testid="stCode"] button:active,
div[data-testid="stCode"] button[title="Copy to clipboard"]:hover {
    background: #FACC15 !important;
    border-color: #EAB308 !important;
    color: #18181B !important;
}

/* Grounding Scenario Reference Callout */
.situation-context-box {
    background: #F5F3EC;
    border-left: 4px solid #FACC15;
    border-top: 1px solid #E7E4DA;
    border-right: 1px solid #E7E4DA;
    border-bottom: 1px solid #E7E4DA;
    border-radius: 0 12px 12px 0;
    padding: 0.85rem 1.1rem;
    margin-bottom: 1.1rem;
    font-size: 0.88rem;
    color: #3F3F46;
    line-height: 1.55;
    word-break: break-word;
}

.situation-context-box strong {
    color: #18181B;
    font-weight: 700;
}

/* Refined Variation Callout */
.refined-container {
    background: #F3E8FF;
    border: 1px solid #E9D5FF;
    border-radius: 10px;
    padding: 0.55rem 0.85rem;
    margin-top: 0.85rem;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.refined-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #FFFFFF;
    color: #6B21A8;
    border: 1px solid #D8B4FE;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Empty State Onboarding Canvas */
.empty-canvas-box {
    background: #FFFFFF;
    border: 1.5px dashed #D6D2C4;
    border-radius: 18px;
    padding: 2.35rem 1.75rem;
    text-align: center;
    margin-top: 0.5rem;
}

.empty-canvas-pill {
    display: inline-block;
    background: #FEF9C3;
    color: #713F12;
    border: 1px solid #FDE047;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.22rem 0.7rem;
    border-radius: 9999px;
    margin-bottom: 0.65rem;
}

.empty-canvas-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #18181B;
    margin-bottom: 0.45rem;
}

.empty-canvas-desc {
    font-size: 0.9rem;
    color: #52525B;
    max-width: 540px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.55;
}

.empty-strategy-preview {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    text-align: left;
}

@media (max-width: 820px) {
    .empty-strategy-preview {
        grid-template-columns: 1fr;
    }
}

.empty-strategy-item {
    background: #FAF9F5;
    border: 1px solid #E7E4DA;
    border-radius: 12px;
    padding: 1rem;
}

.empty-strategy-num {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}

.empty-strategy-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #18181B;
    margin-bottom: 0.25rem;
}

.empty-strategy-text {
    font-size: 0.8rem;
    color: #52525B;
    line-height: 1.45;
}

/* =========================================================================
   Buttons & Interactive Controls (Lemon Yellow Primary, Clean White Secondary)
   ========================================================================= */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.005em !important;
    min-height: 42px !important;
    padding: 0.52rem 1.1rem !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background-color: #FACC15 !important;
    border: 1px solid #EAB308 !important;
    color: #18181B !important;
    box-shadow: 0 3px 12px rgba(250, 204, 21, 0.35) !important;
}

div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background-color: #EAB308 !important;
    border-color: #CA8A04 !important;
    color: #18181B !important;
    box-shadow: 0 5px 16px rgba(234, 179, 8, 0.45) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {
    color: #18181B !important;
    font-weight: 700 !important;
}

div.stButton > button[kind="secondary"],
div[data-testid="stFormSubmitButton"] > button[kind="secondary"],
div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]) {
    background-color: #FFFFFF !important;
    border: 1px solid #E7E4DA !important;
    color: #18181B !important;
    box-shadow: 0 1px 4px rgba(24, 24, 27, 0.03) !important;
}

div.stButton > button[kind="secondary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #FEF9C3 !important;
    border-color: #FACC15 !important;
    color: #18181B !important;
    transform: translateY(-1px) !important;
}

/* Inputs, Textareas, Selectboxes */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background-color: #FAF9F5 !important;
    border: 1px solid #E7E4DA !important;
    border-radius: 12px !important;
    color: #18181B !important;
    font-size: 0.95rem !important;
    line-height: 1.55 !important;
    transition: all 0.18s ease !important;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    background-color: #FFFFFF !important;
    border-color: #EAB308 !important;
    box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.28) !important;
}

[data-baseweb="select"] > div {
    background-color: #FAF9F5 !important;
    border-color: #E7E4DA !important;
    border-radius: 10px !important;
    color: #18181B !important;
    min-height: 42px !important;
}

[data-baseweb="select"] > div:hover {
    border-color: #D6D2C4 !important;
    background-color: #FFFFFF !important;
}

/* =========================================================================
   Expanders & Left-Aligned History Record Headers
   ========================================================================= */
[data-testid="stExpander"] {
    background: #FAF9F5 !important;
    border: 1px solid #E7E4DA !important;
    border-radius: 12px !important;
    margin-bottom: 0.65rem !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

[data-testid="stExpander"]:hover {
    border-color: #D6D2C4 !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    min-height: 46px !important;
    padding: 0.65rem 0.9rem !important;
    font-weight: 600 !important;
    color: #18181B !important;
}

[data-testid="stExpander"] summary > span,
[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"],
[data-testid="stExpander"] summary p {
    text-align: left !important;
    justify-content: flex-start !important;
    margin: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    flex: 1 1 auto !important;
    min-width: 0 !important;
}

/* =========================================================================
   Stat KPI Cards (History & Favourites)
   ========================================================================= */
.stat-kpi-card {
    position: relative;
    background: #FFFFFF;
    border: 1px solid #E7E4DA;
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 4px 16px rgba(24, 24, 27, 0.035);
    overflow: hidden;
    animation: cardFadeIn 0.35s ease-out;
}

.stat-kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: #FACC15;
}

.stat-kpi-val {
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.25rem;
    color: #18181B;
}

.stat-kpi-lbl {
    font-size: 0.75rem;
    font-weight: 700;
    color: #52525B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.stat-kpi-sub {
    font-size: 0.76rem;
    color: #71717A;
    margin-top: 0.25rem;
}

/* Saved Badge Pill */
.saved-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #FEF9C3;
    color: #713F12;
    border: 1px solid #FDE047;
    border-radius: 9999px;
    padding: 0.32rem 0.8rem;
    font-size: 0.78rem;
    font-weight: 700;
}

/* =========================================================================
   Mobile Viewport Refinements (360px, 393px, 440px — below 640px)
   ========================================================================= */
@media (max-width: 639px) {
    .block-container {
        padding-top: 0.7rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-bottom: 2.75rem !important;
    }

    /* Compact single-header card with clean horizontal meta strip */
    .top-nav-shell {
        padding: 0.55rem 0.8rem;
        border-radius: 14px;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .top-nav-brand svg {
        height: 30px !important;
        width: auto !important;
    }

    .top-nav-meta {
        width: 100%;
        justify-content: space-between;
        padding-top: 0.4rem;
        border-top: 1px solid #F0EDE4;
        gap: 0.4rem;
    }

    .top-nav-counts {
        font-size: 0.74rem;
    }

    .top-nav-status-pill {
        padding: 0.22rem 0.6rem;
        font-size: 0.72rem;
    }

    /* 2 x 2 Mobile Navigation Grid via dedicated st.container(key="top_nav_grid") */
    .st-key-top_nav_grid [data-testid="stHorizontalBlock"],
    [class*="st-key-top_nav_grid"] [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 0.45rem !important;
        width: 100% !important;
    }

    .st-key-top_nav_grid [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    .st-key-top_nav_grid [data-testid="stHorizontalBlock"] > [data-testid="column"],
    [class*="st-key-top_nav_grid"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [class*="st-key-top_nav_grid"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        flex: unset !important;
    }

    .st-key-top_nav_grid [data-testid="stButton"],
    [class*="st-key-top_nav_grid"] [data-testid="stButton"] {
        width: 100% !important;
    }

    .st-key-top_nav_grid button,
    [class*="st-key-top_nav_grid"] button {
        width: 100% !important;
        min-height: 44px !important;
        padding: 0.45rem 0.6rem !important;
        font-size: 0.84rem !important;
        white-space: nowrap !important;
    }

    /* Scaled editorial headings & hero */
    .create-hero {
        gap: 0.65rem;
        margin-bottom: 1rem;
    }

    .create-hero-title {
        font-size: 1.5rem !important;
        line-height: 1.2 !important;
    }

    .create-hero-desc {
        font-size: 0.88rem;
    }

    .page-header-container {
        margin-bottom: 1rem;
    }

    .page-header-title {
        font-size: 1.55rem !important;
    }

    .page-header-subtitle {
        font-size: 0.88rem;
    }

    .grounding-chip {
        width: 100%;
        padding: 0.48rem 0.75rem;
        font-size: 0.76rem;
    }

    /* Card & surface spacing */
    [data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:not(.st-key-top_nav_grid) {
        padding: 1rem !important;
        border-radius: 14px !important;
    }

    .empty-canvas-box {
        padding: 1.5rem 1rem;
        border-radius: 14px;
    }

    .empty-canvas-title {
        font-size: 1.1rem;
    }

    /* KPI cards compact & readable */
    .stat-kpi-card {
        padding: 0.85rem 1rem;
    }

    .stat-kpi-val {
        font-size: 1.55rem;
    }

    /* History expander header left-aligned & cleanly truncated */
    [data-testid="stExpander"] summary {
        padding: 0.6rem 0.75rem !important;
        font-size: 0.84rem !important;
    }

    /* Comfortable touch targets across all buttons */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        min-height: 44px !important;
        width: 100% !important;
    }
}

/* Equal-height cards: Technology & Architecture only */
.st-key-tech_frontend_row [data-testid="stHorizontalBlock"],
.st-key-tech_storage_row [data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

.st-key-tech_frontend_row [data-testid="stColumn"],
.st-key-tech_storage_row [data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
    min-width: 0 !important;
}

.st-key-tech_frontend_row [data-testid="stVerticalBlockBorderWrapper"],
.st-key-tech_storage_row [data-testid="stVerticalBlockBorderWrapper"] {
    flex: 1 1 auto !important;
    height: 100% !important;
}

</style>
"""


def inject_custom_css():
    """Inject global ExcuseGPT light editorial SaaS CSS and subtle ambient background orbs."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_html(
        """
        <div class="ambient-canvas" aria-hidden="true">
            <div class="ambient-orb ambient-orb-lemon"></div>
            <div class="ambient-orb ambient-orb-lavender"></div>
            <div class="ambient-orb ambient-orb-peach"></div>
        </div>
        """
    )


def render_html(html_str: str):
    """Render HTML safely into Streamlit without Markdown indentation issues."""
    cleaned = "\n".join(
        line.strip() for line in html_str.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


def get_approach_meta(approach_key: str) -> dict:
    """Return full styling and copy metadata for a given approach key."""
    return APPROACH_METADATA.get(
        approach_key,
        {
            "label": approach_key.replace("_", " ").title(),
            "description": "Context-grounded variation.",
            "badge_bg": "#F5F3EC",
            "badge_color": "#3F3F46",
            "badge_border": "#E7E4DA",
            "accent": "#FACC15",
            "card_tint": "#FAF9F5",
        },
    )


def format_approach_badge(approach_key: str) -> str:
    """Return an HTML pastel approach badge pill for the given approach key."""
    meta = get_approach_meta(approach_key)
    safe_label = html.escape(str(meta["label"]))

    return (
        f'<span class="approach-pill" style="background-color: {meta["badge_bg"]}; '
        f'color: {meta["badge_color"]}; border: 1px solid {meta["badge_border"]};">'
        f'{safe_label}</span>'
    )


def get_approach_description(approach_key: str) -> str:
    """Return the human-readable strategy explanation for an approach."""
    return get_approach_meta(approach_key)["description"]


def render_stat_kpi(label: str, value: str | int, subtitle: str = ""):
    """Render a crisp white SaaS KPI metric card with a lemon accent bar."""
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    sub_html = f'<div class="stat-kpi-sub">{html.escape(str(subtitle))}</div>' if subtitle else ""
    render_html(
        f"""
        <div class="stat-kpi-card">
            <div class="stat-kpi-val">{safe_value}</div>
            <div class="stat-kpi-lbl">{safe_label}</div>
            {sub_html}
        </div>
        """
    )


def render_page_header(badge: str, title: str, subtitle: str = ""):
    """Render a unified editorial page header across views."""
    safe_badge = html.escape(str(badge))
    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))
    sub_html = f'<p class="page-header-subtitle">{safe_subtitle}</p>' if subtitle else ""
    render_html(
        f"""
        <div class="page-header-container">
            <div class="page-header-badge">{safe_badge}</div>
            <h1 class="page-header-title">{safe_title}</h1>
            {sub_html}
        </div>
        """
    )