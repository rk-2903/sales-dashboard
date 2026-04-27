# ================================
# REQUIRED LIBRARIES
# pip install streamlit pandas openpyxl plotly
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Sales Intelligence",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# -------------------------
# GLOBAL STYLES
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

/* ===== STREAMLIT CHROME ===== */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; height: 0; }

/* Dark header */
[data-testid="stHeader"] {
    background: #060a18 !important;
    border-bottom: 1px solid #1a2236 !important;
}

.st-emotion-cache-5r6ut5 {
    color: white !important;
}
            
/* Force all header elements visible */
[data-testid="stHeader"] * {
    visibility: visible !important;
    opacity: 1 !important;
}
/* Sidebar toggle buttons — base layer (JS below overrides inline) */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    visibility: visible !important;
    opacity: 1 !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* ===== BASE ===== */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ===== APP BACKGROUND ===== */
.stApp {
    background: linear-gradient(160deg, #060a18 0%, #080d1c 40%, #0a0f22 70%, #07090f 100%) !important;
    background-attachment: fixed !important;
    color: #e2e8f0;
    min-height: 100vh;
}

/* ===== SIDEBAR — force dark on every possible div ===== */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div > div,
section[data-testid="stSidebar"] > div > div > div {
    background-color: #090d1e !important;
    background:       #090d1e !important;
}
section[data-testid="stSidebar"] {
    border-right: 1px solid #1a2236 !important;
    min-width: 360px !important;
    width: 380px !important;
    max-width: 380px !important;
}
/* Remove inner horizontal padding so tags use the full width */
section[data-testid="stSidebar"] > div:first-child {
    padding-left: 12px !important;
    padding-right: 12px !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
            
.st-es {
    padding-right: 0 !important;
}

/* All text inside sidebar */
section[data-testid="stSidebar"] * { color: #8899b4 !important; }

/* Make tag × close buttons always visible and clickable */
section[data-testid="stSidebar"] [data-baseweb="tag"] button,
section[data-testid="stSidebar"] [data-baseweb="tag"] [aria-label="Remove"],
section[data-testid="stSidebar"] [data-baseweb="tag"] span[role="img"] {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: all !important;
    cursor: pointer !important;
    color: #93c5fd !important;
    fill: #93c5fd !important;
}

/* Nav radio */
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio label {
    padding: 9px 14px !important;
    border-radius: 9px !important;
    font-size: 0.88rem !important;
    transition: all 0.18s;
    cursor: pointer;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #141929 !important;
    color: #e2e8f0 !important;
}

/* Multiselect tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #1a2d50 !important;
    border: 1px solid #2a4070 !important;
    border-radius: 6px !important;
    max-width: 100% !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    flex-shrink: 1 !important;
    flex-grow: 0 !important;
    padding: 2px 4px 2px 8px !important;
    font-size: 0.78rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 2px !important;
    box-sizing: border-box !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #93c5fd !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    display: inline-block !important;
    font-size: 0.78rem !important;
    max-width: calc(100% - 20px) !important;
    min-width: 0 !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] svg,
section[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] {
    color: #93c5fd !important;
    fill: #93c5fd !important;
    flex-shrink: 0 !important;
    display: inline-block !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: all !important;
    cursor: pointer !important;
    min-width: 14px !important;
    min-height: 14px !important;
}
/* Multiselect input box — contained, wraps tags neatly */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    flex-wrap: wrap !important;
    max-height: 160px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 6px 8px !important;
    gap: 0px !important;
    scrollbar-width: thin !important;
    scrollbar-color: #1e2d4a #090d1e !important;
    box-sizing: border-box !important;
    width: 100% !important;
}
/* The inner flex row that holds tags — Streamlit gives it a negative margin
   to simulate gap; this clips the first tag on the left. Reset it. */
section[data-testid="stSidebar"] [data-baseweb="select"] > div > div:first-child {
    flex-wrap: wrap !important;
    overflow: visible !important;
    gap: 4px !important;
    width: 100% !important;
    min-width: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-left: 0 !important;
    padding-top: 2px !important;
}
/* Every direct child span/div inside that row (the tag wrappers) */
section[data-testid="stSidebar"] [data-baseweb="select"] > div > div:first-child > span,
section[data-testid="stSidebar"] [data-baseweb="select"] > div > div:first-child > div {
    margin-left: 0 !important;
    margin-top: 2px !important;
    margin-bottom: 2px !important;
    margin-right: 4px !important;
}

/* Sidebar selects / inputs */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #0f1628 !important;
    border-color: #1e2d4a !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
section[data-testid="stSidebar"] input {
    # background: #0f1628 !important;
    border-color: #1e2d4a !important;
    color: #e2e8f0 !important;
}

/* ===== SLIDER (visible on dark bg) ===== */
/* Track */
[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    background: #1e2d4a !important;
}
/* Filled portion */
[data-testid="stSlider"] [role="progressbar"] {
    background: #3b82f6 !important;
}
/* Thumb */
[data-testid="stSlider"] [role="slider"] {
    background:   #60a5fa !important;
    border-color: #60a5fa !important;
    box-shadow:   0 0 0 4px rgba(96,165,250,0.25) !important;
}
/* Labels */
[data-testid="stSlider"] p,
[data-testid="stSlider"] label { color: #8899b4 !important; }

/* ===== PAGE TITLES ===== */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.9rem !important;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    margin-bottom: 0.1rem !important;
}
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #cbd5e1 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
}

/* ===== METRIC CARDS ===== */
[data-testid="metric-container"] {
    background: linear-gradient(140deg, #0f1628, #131c30);
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 18px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(96,165,250,0.12);
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #60a5fa !important;
    white-space: nowrap !important;
    overflow: visible !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8 !important;   /* was #4a6080 — much more visible */
    font-weight: 600 !important;
}
/* Delta label */
[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid #1a2236 !important;
}

/* ===== INPUTS (main content) ===== */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div {
    background: #0f1628 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 9px !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: #0f1628 !important;
    border: 1px solid #1e2d4a !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* ===== INPUT / SELECTBOX / NUMBER-INPUT LABELS (main content) ===== */
/* The label above every widget */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSlider"] label,
.stSelectbox label,
.stMultiSelect label,
.stNumberInput label,
.stDateInput label,
div[data-baseweb="form-control"] > label,
p[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] {
    color: #93c5fd !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 4px !important;
}

/* Selectbox selected value text */
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {
    # color: #e2e8f0 !important;
}

/* Number input +/- buttons */
[data-testid="stNumberInput"] button {
    background: #1a2744 !important;
    border-color: #1e2d4a !important;
    color: #60a5fa !important;
}

/* ===== HIDE ALL "No results" / "You can only select" POPOVER BOXES ===== */
/* Hide every layer/popover that contains only a no-results or max-select message */
[data-baseweb="layer"]:has([data-baseweb="menu"]),
[data-baseweb="layer"]:has([role="listbox"]) {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}
/* But show it again if it has real selectable options */
[data-baseweb="layer"]:has([role="option"]:not([aria-disabled="true"])) {
    display: block !important;
    visibility: visible !important;
    pointer-events: all !important;
    opacity: 1 !important;
    height: auto !important;
    overflow: visible !important;
}
/* Hide empty listboxes and no-results containers */
[role="listbox"]:empty,
[data-baseweb="menu"]:empty,
[data-baseweb="no-results"],
[data-baseweb="popover"] [data-baseweb="menu"]:has(li[aria-disabled="true"]:only-child),
[data-baseweb="popover"] ul:has(li[aria-disabled="true"]:only-child) {
    display: none !important;
}
/* Style real popover/menu dropdowns (when they have actual options) */
[data-baseweb="popover"],
[data-baseweb="popover"] > div {
    background: #0f1628 !important;
    border: 1px solid #1e2d4a !important;
}
[data-baseweb="popover"] [role="option"] {
    color: #c8d8f0 !important;
    background: #0f1628 !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background: #1a2744 !important;
    color: #ffffff !important;
}

/* ===== SELECT ALL / CLEAR ALL BUTTONS (sidebar) ===== */
section[data-testid="stSidebar"] .stButton button {
    background: #0d1424 !important;
    color: #6b8ab0 !important;
    border: 1px solid #1a2640 !important;
    border-radius: 5px !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    padding: 2px 6px !important;
    height: 24px !important;
    min-height: 24px !important;
    line-height: 1 !important;
    letter-spacing: 0.02em !important;
    transition: background 0.15s !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #131c30 !important;
    border-color: #2a3f60 !important;
    color: #93c5fd !important;
}

/* ===== DOWNLOAD BUTTONS ===== */
.stDownloadButton button {
    background: linear-gradient(135deg, #1d4ed8, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1rem !important;
    transition: opacity 0.2s !important;
}
.stDownloadButton button:hover { opacity: 0.82 !important; }

/* Table download button — inline, right-aligned */
.tbl-dl-row {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
    margin-top: -4px;
}

/* ===== SECTION CARDS ===== */
.section-card {
    border-radius: 14px;
    padding: 18px 22px 6px 22px;
    margin-bottom: 4px;
    border: 1px solid #1a2236;
}
.card-blue   { background: linear-gradient(145deg, #0a1020, #0f1830); border-color: #1a2d50; }
.card-purple { background: linear-gradient(145deg, #0d0a1e, #120f2a); border-color: #251d45; }
.card-teal   { background: linear-gradient(145deg, #080f18, #091519); border-color: #0f2230; }
.card-orange { background: linear-gradient(145deg, #110c08, #180f0a); border-color: #2e1e10; }
.card-rose   { background: linear-gradient(145deg, #120810, #1a0c15); border-color: #30152a; }
.card-green  { background: linear-gradient(145deg, #080f0c, #09140f); border-color: #0e2a1a; }
.card-slate  { background: linear-gradient(145deg, #0a0d12, #0f1218); border-color: #1a1f2e; }

/* ===== SECTION HEADER ===== */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1a2236;
}

/* ===== BADGE ===== */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}
.badge-blue   { background: rgba(96,165,250,0.12); color: #93c5fd; border: 1px solid rgba(96,165,250,0.25); }
.badge-purple { background: rgba(167,139,250,0.12); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.25); }
.badge-teal   { background: rgba(45,212,191,0.12);  color: #5eead4; border: 1px solid rgba(45,212,191,0.25); }
.badge-orange { background: rgba(251,146,60,0.12);  color: #fdba74; border: 1px solid rgba(251,146,60,0.25); }
.badge-rose   { background: rgba(244,114,182,0.12); color: #f9a8d4; border: 1px solid rgba(244,114,182,0.25); }
.badge-green  { background: rgba(52,211,153,0.12);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.25); }

/* ===== DIVIDER ===== */
.section-divider { height: 32px; border-left: none; }

/* ===== CLEAR FILTERS BUTTON ===== */
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #7f1d1d, #991b1b) !important;
    color: #fca5a5 !important;
    border: 1px solid #b91c1c !important;
    border-radius: 9px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 0.45rem !important;
    transition: all 0.2s !important;
    margin-bottom: 10px !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, #991b1b, #b91c1c) !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(239,68,68,0.4) !important;
}

/* =====================================================
   MOBILE — phones ≤ 480px
   ===================================================== */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.75rem !important;
    }
    h1 { font-size: 1.2rem !important; }
    h2, h3 { font-size: 0.82rem !important; }
    [data-testid="metric-container"] { padding: 10px 12px !important; border-radius: 10px; }
    [data-testid="stMetricValue"]    { font-size: 1.0rem !important; }
    [data-testid="stMetricLabel"]    { font-size: 0.58rem !important; }
    [data-testid="stHorizontalBlock"]        { flex-wrap: wrap !important; }
    [data-testid="stHorizontalBlock"] > div  { min-width: 48% !important; flex: 1 1 48% !important; }
    .section-card   { padding: 10px 12px 4px 12px !important; border-radius: 10px !important; }
    .section-header { gap: 5px !important; margin-bottom: 8px !important; }
    [data-testid="stDataFrame"]  { overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }
    [data-testid="stMultiSelect"],
    [data-testid="stSelectbox"],
    [data-testid="stNumberInput"],
    [data-testid="stDateInput"],
    [data-testid="stSlider"]    { width: 100% !important; }
    .js-plotly-plot { touch-action: pan-x pan-y !important; }
    .badge { font-size: 0.58rem !important; padding: 2px 6px !important; }
    .section-divider { height: 14px; }
}

/* =====================================================
   TABLET — 481 – 900px
   ===================================================== */
@media (min-width: 481px) and (max-width: 900px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    h1 { font-size: 1.5rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.3rem !important; }
    [data-testid="stDataFrame"]   { overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }
    .js-plotly-plot { touch-action: pan-x pan-y !important; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR TOGGLE BUTTON FIX (JavaScript injection)
# CSS alone cannot reliably override Streamlit's inline styles on these buttons.
# We use a MutationObserver to watch the DOM and apply bright styling directly.
# -------------------------
st.markdown("""
<style>
/* Glowing toggle button styles applied via JS below */
.sidebar-toggle-styled {
    background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 100%) !important;
    border-radius: 50% !important;
    border: 2.5px solid #60a5fa !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.3), 0 0 16px rgba(96,165,250,0.7), 0 4px 12px rgba(0,0,0,0.8) !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
</style>
<script>
(function() {
    function styleToggleBtn(btn) {
        if (!btn) return;
        // Container styling
        btn.style.cssText = [
            'background: linear-gradient(135deg, #1d4ed8, #7c3aed)',
            'border-radius: 50%',
            'border: 2.5px solid #60a5fa',
            'box-shadow: 0 0 0 3px rgba(96,165,250,0.3), 0 0 18px rgba(96,165,250,0.75), 0 4px 14px rgba(0,0,0,0.8)',
            'width: 40px',
            'height: 40px',
            'min-width: 40px',
            'min-height: 40px',
            'display: flex',
            'align-items: center',
            'justify-content: center',
            'cursor: pointer',
            'position: relative',
            'z-index: 99999',
            'transition: box-shadow 0.2s, transform 0.15s'
        ].join('; ');

        // SVG / icon inside
        const svgs = btn.querySelectorAll('svg, path, polyline, line');
        svgs.forEach(el => {
            el.style.cssText = 'color:#ffffff; fill:#ffffff; stroke:#ffffff; width:18px; height:18px;';
        });

        // Hover effect
        btn.onmouseenter = function() {
            this.style.boxShadow = '0 0 0 5px rgba(96,165,250,0.4), 0 0 28px rgba(96,165,250,1), 0 6px 18px rgba(0,0,0,0.9)';
            this.style.transform = 'scale(1.12)';
        };
        btn.onmouseleave = function() {
            this.style.boxShadow = '0 0 0 3px rgba(96,165,250,0.3), 0 0 18px rgba(96,165,250,0.75), 0 4px 14px rgba(0,0,0,0.8)';
            this.style.transform = 'scale(1)';
        };
    }

    function applyPulse(btn) {
        if (!btn) return;
        let growing = true;
        setInterval(function() {
            if (!document.body.contains(btn)) return;
            if (growing) {
                btn.style.boxShadow = '0 0 0 6px rgba(96,165,250,0.15), 0 0 26px rgba(96,165,250,0.9), 0 4px 14px rgba(0,0,0,0.8)';
            } else {
                btn.style.boxShadow = '0 0 0 3px rgba(96,165,250,0.3), 0 0 18px rgba(96,165,250,0.75), 0 4px 14px rgba(0,0,0,0.8)';
            }
            growing = !growing;
        }, 1100);
    }

    function findAndStyle() {
        // Collapsed-state expand button
        const collapsed = document.querySelector('[data-testid="collapsedControl"]');
        if (collapsed) {
            styleToggleBtn(collapsed);
            applyPulse(collapsed);  // pulse only on the expand button so user notices it
        }

        // Expanded-state collapse button
        const collapseBtn = document.querySelector('[data-testid="stSidebarCollapseButton"]');
        if (collapseBtn) {
            styleToggleBtn(collapseBtn);
        }
    }

    // ── Aggressively hide the white "No results" dropdown popup ──
    function hideEl(el) {
        if (!el || el._bwHidden) return;
        el._bwHidden = true;
        el.style.cssText += ';display:none!important;visibility:hidden!important;' +
            'opacity:0!important;height:0!important;max-height:0!important;' +
            'overflow:hidden!important;pointer-events:none!important;' +
            'position:fixed!important;top:-99999px!important;left:-99999px!important;' +
            'width:0!important;max-width:0!important;';
        // Re-hide if Streamlit restores styles
        var obs = new MutationObserver(function() {
            if (el.style.display !== 'none') {
                el.style.setProperty('display', 'none', 'important');
                el.style.setProperty('top', '-99999px', 'important');
            }
        });
        obs.observe(el, { attributes: true, attributeFilter: ['style'] });
    }
    function hideWithParents(el) {
        if (!el) return;
        hideEl(el);
        var p = el.parentElement;
        for (var i = 0; i < 12 && p && p !== document.body; i++) {
            var bw = p.getAttribute('data-baseweb') || '';
            if (bw === 'layer' || bw === 'popover' || bw === 'menu') {
                hideEl(p); return;
            }
            p = p.parentElement;
        }
    }
    function fixNoResultsBox() {
        // Walk every element looking for the bad messages
        var badPhrases = ['No results', 'You can only select'];
        
        function isBadText(t) {
            return badPhrases.some(function(b) { return t.indexOf(b) !== -1; });
        }

        // Find text nodes containing bad phrases and hide their ancestor popup
        function walkAndHide(root) {
            var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
            var node;
            while ((node = walker.nextNode())) {
                var t = (node.nodeValue || '').trim();
                if (!isBadText(t)) continue;
                // Found bad text — walk up to find the floating container
                var el = node.parentElement;
                for (var i = 0; i < 15 && el && el !== document.body; i++) {
                    var bw = el.getAttribute('data-baseweb') || '';
                    var role = el.getAttribute('role') || '';
                    var tag = el.tagName || '';
                    var s = window.getComputedStyle(el);
                    // Hide at the layer/popover level, or any positioned floating box
                    if (bw === 'layer' || bw === 'popover' || bw === 'menu' || role === 'listbox' ||
                        ((s.position === 'fixed' || s.position === 'absolute') && parseInt(s.zIndex||0) > 50)) {
                        hideEl(el);
                        break;
                    }
                    el = el.parentElement;
                }
            }
        }
        walkAndHide(document.documentElement);
    }
    setInterval(fixNoResultsBox, 40);

    // Run instantly on every DOM mutation
    var noResObserver = new MutationObserver(function(mutations) {
        // Only process if something was added
        for (var i = 0; i < mutations.length; i++) {
            if (mutations[i].addedNodes.length > 0) { fixNoResultsBox(); break; }
        }
    });
    noResObserver.observe(document.documentElement, { childList: true, subtree: true });

    const observer = new MutationObserver(function() {
        findAndStyle();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Also run on a short interval as a safety net
    setInterval(findAndStyle, 800);
})();
</script>
""", unsafe_allow_html=True)

# -------------------------
# PLOTLY THEME HELPERS
# -------------------------
COLORS = ["#60a5fa", "#a78bfa", "#f472b6", "#34d399", "#fbbf24", "#fb923c", "#5eead4"]
PAPER_BG = "rgba(10,14,24,0.97)"
GRID = "#1a2236"
FONT_C = "#7a90aa"

def _fmt_axis_tick(val):
    """Return compact label for a plotly axis tick value."""
    if abs(val) >= 1_000_000_000: return f"{val/1_000_000_000:.2f}B"
    if abs(val) >= 1_000_000:     return f"{val/1_000_000:.2f}M"
    if abs(val) >= 1_000:         return f"{val/1_000:.1f}K"
    return str(int(val))

def theme(fig, h=340):
    fig.update_layout(
        height=h,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#c8d8f0", size=12),
        margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(
            bgcolor="rgba(8,14,32,0.96)",
            bordercolor="#2a3f60",
            borderwidth=1,
            font=dict(size=12, color="#e2e8f0"),
            title=dict(font=dict(color="#93c5fd", size=12)),
        ),
        xaxis=dict(
            gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID,
            tickfont=dict(color="#94a3b8", size=11),
            title_font=dict(color="#94a3b8"),
        ),
        yaxis=dict(
            gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID,
            tickfont=dict(color="#94a3b8", size=11),
            title_font=dict(color="#94a3b8"),
            # Compact tick labels: 55.77M, 10.50K, etc.
            tickformat=",.2s",           # SI suffix: 55.8M  (Plotly built-in)
            exponentformat="none",
        ),
    )
    return fig

def fmt_num(n):
    """Format sales number compactly always in M with 2 decimals: 677899 → ₹0.68M"""
    try: n = float(n)
    except: return str(n)
    if abs(n) >= 1_000_000_000: return f"\u20b9{n/1_000_000_000:.2f}B"
    if abs(n) >= 1_000:         return f"\u20b9{n/1_000_000:.2f}M"
    return f"\u20b9{int(n):,}"

def fmt_count(n):
    """Format count compactly without currency symbol."""
    try: n = float(n)
    except: return str(n)
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.2f}K"
    return f"{int(n):,}"

def sec_html(label, badge_label, badge_cls="badge-blue", icon=""):
    return f"""
    <div class="section-header">
        <span style="font-size:1.1rem;">{icon}</span>
        <h2>{label}</h2>
        <span class="badge {badge_cls}">{badge_label}</span>
    </div>"""

def divider():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False, ttl=600)
def _to_excel_bytes(df_export):
    buf = io.BytesIO()
    df_export.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    return buf.getvalue()

def excel_download(df_export, filename, label="⬇ Download as Excel"):
    """Render a styled Excel download button — Excel generation is cached."""
    st.download_button(
        label=label,
        data=_to_excel_bytes(df_export),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def load_data():
    df = pd.read_excel(
        "/Users/rahul/Downloads/sales-report/sample_sales_data.xlsx",
        engine="openpyxl"
    )
    df.columns = df.columns.str.strip()
    for col in ["Date","Channel","SKU","TotalSales","OrderCount"]:
        if col not in df.columns:
            st.error(f"❌ Missing column: **{col}**"); st.stop()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["TotalSales"] = df["TotalSales"].round(0).astype(int)
    df["OrderCount"] = df["OrderCount"].round(0).astype(int)
    return df

# ── Fast pre-aggregations cached independently so page switches are instant ──
@st.cache_data(show_spinner=False, ttl=3600)
def precompute(df):
    daily        = df.groupby("Date")[["TotalSales","OrderCount"]].sum().reset_index()
    monthly_ch   = df.groupby(["Month","Channel"])["TotalSales"].sum().reset_index()
    ch_split     = df.groupby("Channel")["TotalSales"].sum().reset_index()
    return daily, monthly_ch, ch_split

with st.spinner("Loading data…"):
    df = load_data()

_pre_daily, _pre_monthly_ch, _pre_ch_split = precompute(df)

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 4px 14px 4px;border-bottom:1px solid #1a2236;margin-bottom:14px;">
        <div style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:800;
                    background:linear-gradient(135deg,#60a5fa,#a78bfa);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;letter-spacing:-0.01em;">
            ⚡ SalesIQ
        </div>
        <div style="font-size:0.68rem;color:#2d3f58;margin-top:2px;
                    letter-spacing:0.1em;text-transform:uppercase;">
            Intelligence Dashboard
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;color:#2d3f58;margin-bottom:6px;">NAVIGATION</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "🏠  Overview",
        "📅  Day-on-Day",
        "🗓️  Month-on-Month",
        "📦  SKU Day-on-Day",
        "📊  SKU Month-on-Month",
        "🏆  Top SKUs",
        "🆕  New SKUs",
        "⚠️  Zero Sales Alert",
        "🤖  Ask Questions",
    ], label_visibility="collapsed")

    st.markdown('<hr style="border-color:#1a2236;margin:14px 0;">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;color:#2d3f58;margin-bottom:6px;margin-left:14px;">FILTERS_ABC</div>', 
        unsafe_allow_html=True)

    all_channels = sorted(df["Channel"].unique())

    channels = st.multiselect(
        "Channel_ABC",
        all_channels,
        default=all_channels,
        key="channels_sel",
    )
    if not channels:
        channels = all_channels

    all_skus = sorted(df["SKU"].unique())

    # Select All / Clear All — set default before widget renders to avoid double rerun
    if "sku_sel" not in st.session_state:
        st.session_state["sku_sel"] = []
    sku_col1, sku_col2 = st.columns(2)
    if sku_col1.button("Select All", use_container_width=True, key="sku_all"):
        st.session_state["sku_sel"] = all_skus
        st.rerun()
    if sku_col2.button("Clear All", use_container_width=True, key="sku_clear"):
        st.session_state["sku_sel"] = []
        st.rerun()

    sku_filter = st.multiselect(
        "Search SKU",
        all_skus,
        default=st.session_state["sku_sel"],
        key="sku_sel",
    )
    date_range = st.date_input(
        "Date Range",
        value=[df["Date"].min(), df["Date"].max()],
        key="date_sel",
    )
    threshold  = st.selectbox(
        "Change Threshold %",
        [5,10,15,20],
        index=0,
        key="threshold_sel",
    )

    st.markdown('<hr style="border-color:#1a2236;margin:14px 0;">', unsafe_allow_html=True)

# -------------------------
# FILTER DATA  (fast-path: skip SKU filter when all selected)
# -------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def filter_df(df, channels_tuple, sku_tuple, d_min, d_max):
    mask = (
        df["Channel"].isin(channels_tuple) &
        (df["Date"] >= pd.to_datetime(d_min)) &
        (df["Date"] <= pd.to_datetime(d_max))
    )
    out = df[mask]
    if sku_tuple:  # empty tuple = no SKU filter = all SKUs
        out = out[out["SKU"].isin(sku_tuple)]
    return out

_sku_tuple = tuple(sku_filter) if sku_filter and len(sku_filter) < len(df["SKU"].unique()) else ()
df_f = filter_df(df, tuple(channels), _sku_tuple, date_range[0], date_range[1])

@st.cache_data(show_spinner=False, ttl=600)
def make_excel(df_export):
    buf = io.BytesIO()
    df_export.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    return buf.getvalue()

with st.sidebar:
    st.download_button(
        "⬇  Download Filtered Data",
        data=make_excel(df_f),
        file_name="sales_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# -------------------------
# CACHED PAGE AGGREGATIONS  — all heavy groupby ops run once per filter combo
# -------------------------
@st.cache_data(show_spinner=False, ttl=600)
def page_aggs(df_in):
    """Pre-compute all aggregations every page needs. Cached per unique df_in."""
    aggs = {}
    # Overview
    aggs["daily_trend"]   = df_in.groupby("Date")["TotalSales"].sum().reset_index()
    aggs["ch_split"]      = df_in.groupby("Channel")["TotalSales"].sum().reset_index()
    aggs["monthly_trend"] = df_in.groupby("Month")["TotalSales"].sum().reset_index()

    # Day-on-Day
    daily_ch = (df_in.groupby(["Date","Channel"])[["TotalSales","OrderCount"]].sum().reset_index().sort_values(["Channel","Date"]))
    daily_ch["Prev Sales"] = daily_ch.groupby("Channel")["TotalSales"].shift(1).fillna(0).astype(int)
    aggs["daily_ch"] = daily_ch

    # Month-on-Month
    aggs["monthly_ch"] = df_in.groupby(["Month","Channel"])[["TotalSales","OrderCount"]].sum().reset_index()

    # SKU Day-on-Day
    sku_daily = (df_in.groupby(["Date","SKU"])[["TotalSales","OrderCount"]].sum().reset_index().sort_values(["SKU","Date"]))
    sku_daily["Prev Sales"] = sku_daily.groupby("SKU")["TotalSales"].shift(1).fillna(0).astype(int)
    aggs["sku_daily"] = sku_daily

    # SKU Month-on-Month
    aggs["sku_monthly"] = df_in.groupby(["Month","SKU"])[["TotalSales","OrderCount"]].sum().reset_index()

    # Top SKUs
    aggs["sku_total"] = df_in.groupby("SKU")[["TotalSales","OrderCount"]].sum().reset_index()

    # Metrics
    aggs["ts"]   = int(df_in["TotalSales"].sum())
    aggs["to_"]  = int(df_in["OrderCount"].sum())
    aggs["asku"] = int(df_in["SKU"].nunique())

    return aggs

_aggs = page_aggs(df_f)

# -------------------------
# STYLE FUNCTIONS
# -------------------------
def style_change(val):
    if val == "" or pd.isna(val): return ""
    try: num = int(str(val).replace("%",""))
    except: return ""
    if num >= threshold:  return "background-color:rgba(52,211,153,0.15);color:#34d399;font-weight:600"
    if num <= -threshold: return "background-color:rgba(248,113,113,0.15);color:#f87171;font-weight:600"
    return "color:#64748b"

def style_prev(val):
    if val == "Previous": return "background-color:rgba(20,25,40,0.8);color:#475569"
    return ""

# ======================================================
# OVERVIEW
# ======================================================
if page == "🏠  Overview":
    st.title("Sales Intelligence")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Real-time performance across all channels</p>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    ts   = _aggs["ts"]
    to_  = _aggs["to_"]
    asku = _aggs["asku"]
    aov  = ts//to_ if to_ else 0
    c1.metric("💰 Total Sales",      fmt_num(ts))
    c2.metric("📦 Total Orders",     fmt_count(to_))
    c3.metric("🏷️ Active SKUs",      fmt_count(asku))
    c4.metric("📈 Avg Order Value",  fmt_num(aov))

    divider()

    # Daily Sales Trend
    st.markdown(f'<div class="section-card card-blue">{sec_html("Daily Sales Trend","Daily","badge-blue","📈")}</div>', unsafe_allow_html=True)
    daily_trend = _aggs["daily_trend"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_trend["Date"], y=daily_trend["TotalSales"],
        mode="lines", line=dict(color="#fa607a", width=2.5),
        fill="tozeroy", fillcolor="rgba(96,165,250,0.06)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>₹%{y:,.0f}<extra></extra>"
    ))
    theme(fig, 300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    lc, rc = st.columns(2)
    with lc:
        st.markdown(f'<div class="section-card card-purple">{sec_html("Sales by Channel","Split","badge-purple","🍩")}</div>', unsafe_allow_html=True)
        ch_split = _aggs["ch_split"]
        # Vivid neon colors for pie slices
        PIE_COLORS = ["#f472b6","#a78bfa","#34d399","#fbbf24","#fb923c","#60a5fa","#5eead4","#f87171","#c084fc"]
        fig2 = go.Figure(go.Pie(
            labels=ch_split["Channel"], values=ch_split["TotalSales"],
            hole=0.55,
            marker=dict(
                colors=PIE_COLORS[:len(ch_split)],
                line=dict(color="#060a18", width=2)
            ),
            textfont=dict(size=13, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>"
        ))
        fig2.update_layout(
            height=320, paper_bgcolor=PAPER_BG,
            font=dict(family="DM Sans", color="#e2e8f0"),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(8,14,32,0.96)", bordercolor="#2a1f4a", borderwidth=1,
                font=dict(size=12, color="#e2e8f0"),
                orientation="v", x=1.02, y=0.5,
            ),
            margin=dict(l=8,r=130,t=8,b=8),
            annotations=[dict(text="<b>Revenue</b>",x=0.5,y=0.5,
                              font=dict(size=12,color="#94a3b8"),showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with rc:
        st.markdown(f'<div class="section-card card-teal">{sec_html("Monthly Revenue by Channel","MoM","badge-teal","📊")}</div>', unsafe_allow_html=True)
        # Filter pre-aggregated monthly data to current filters
        active_months = sorted(df_f["Month"].unique())
        monthly_ch = _pre_monthly_ch[
            (_pre_monthly_ch["Month"].isin(active_months)) &
            (_pre_monthly_ch["Channel"].isin(channels))
        ]
        # Vivid neon bar colors per channel
        BAR_COLORS = ["#f472b6","#a78bfa","#34d399","#fbbf24","#fb923c","#60a5fa","#5eead4","#f87171","#c084fc"]
        fig3 = px.bar(monthly_ch, x="Month", y="TotalSales", color="Channel",
                      color_discrete_sequence=BAR_COLORS, barmode="group",
                      labels={"TotalSales":"Revenue (₹)","Month":""})
        theme(fig3, 320)
        fig3.update_traces(marker_line_width=0, opacity=1.0)
        # Always show first and last month on x-axis
        _all_months = sorted(monthly_ch["Month"].unique())
        _tick_vals  = sorted(set([_all_months[0], _all_months[-1]] + _all_months))
        fig3.update_layout(
            bargap=0.25, bargroupgap=0.05,
            legend=dict(bgcolor="rgba(8,14,32,0.96)", bordercolor="#1a2d3a",
                        borderwidth=1, font=dict(size=12, color="#e2e8f0")),
            xaxis=dict(
                tickmode="array",
                tickvals=_tick_vals,
                ticktext=_tick_vals,
                tickfont=dict(color="#94a3b8", size=11),
            ),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ======================================================
# DAY-ON-DAY
# ======================================================
elif page == "📅  Day-on-Day":
    st.title("Day-on-Day")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Daily sales performance vs previous day by channel</p>', unsafe_allow_html=True)

    daily = _aggs["daily_ch"].copy()
    daily["Change %"] = ((daily["TotalSales"]-daily["Prev Sales"])/daily["Prev Sales"].replace(0,pd.NA)*100).round(0)
    daily["Change %"] = daily["Change %"].apply(lambda x: f"{int(x)}%" if pd.notna(x) else "")

    st.markdown(f'<div class="section-card card-blue">{sec_html("Daily Trend by Channel","Chart","badge-blue","📈")}</div>', unsafe_allow_html=True)
    chart_df = _aggs["daily_ch"][["Date","Channel","TotalSales"]].copy()
    fig = px.line(chart_df, x="Date", y="TotalSales", color="Channel",
                  color_discrete_sequence=COLORS,
                  labels={"TotalSales":"Revenue (₹)","Date":""}, markers=True)
    theme(fig, 340)
    fig.update_traces(line=dict(width=2), marker=dict(size=4))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    st.markdown(f'<div class="section-card card-purple">{sec_html("Detailed Data Table","Table","badge-purple","📋")}</div>', unsafe_allow_html=True)
    daily_export = daily.copy()
    daily_export["Date"] = daily_export["Date"].dt.strftime("%Y-%m-%d")
    excel_download(daily_export, "day_on_day.xlsx")
    st.dataframe(daily_export.style.applymap(style_change, subset=["Change %"]),
                 use_container_width=True, height=400)

# ======================================================
# MONTH-ON-MONTH
# ======================================================
elif page == "🗓️  Month-on-Month":
    st.title("Month-on-Month")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Channel-wise revenue comparison across months</p>', unsafe_allow_html=True)

    months = sorted(df_f["Month"].unique())
    c1,c2,c3,c4 = st.columns(4)
    prev_month = c1.selectbox("Previous Month", months, index=max(0,len(months)-2))
    curr_month = c2.selectbox("Current Month",  months, index=len(months)-1)
    start_day  = c3.number_input("Start Day", 1, 31, 1)
    end_day    = c4.number_input("End Day",   1, 31, 18)

    rows = []
    for channel in sorted(df_f["Channel"].unique()):
        prev_val = curr_val = 0
        for label, month in [("Previous",prev_month),("Current",curr_month)]:
            ms    = pd.to_datetime(f"{month}-01")
            ld    = (ms+pd.offsets.MonthEnd()).day
            s     = ms.replace(day=min(start_day,ld))
            e     = ms.replace(day=min(end_day,ld))
            total = df_f[(df_f["Channel"]==channel)&(df_f["Date"]>=s)&(df_f["Date"]<=e)]["TotalSales"].sum()
            rows.append({"Channel":channel,"Period":label,"Date Range":f"{s:%Y-%m-%d} → {e:%Y-%m-%d}","Total Sales":int(total),"Change %":""})
            if label=="Previous": prev_val=total
            else: curr_val=total
        if prev_val!=0: rows[-1]["Change %"]=f"{int(((curr_val-prev_val)/prev_val)*100)}%"

    mom      = pd.DataFrame(rows)
    curr_rows = mom[mom["Period"]=="Current"].copy()
    prev_rows = mom[mom["Period"]=="Previous"].copy()

    divider()

    st.markdown(f'<div class="section-card card-teal">{sec_html("Revenue Comparison by Channel","Chart","badge-teal","📊")}</div>', unsafe_allow_html=True)
    compare_df = pd.merge(
        prev_rows[["Channel","Total Sales"]].rename(columns={"Total Sales":"Previous"}),
        curr_rows[["Channel","Total Sales"]].rename(columns={"Total Sales":"Current"}),
        on="Channel"
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Previous", x=compare_df["Channel"], y=compare_df["Previous"], marker_color=COLORS[1], opacity=0.7))
    fig.add_trace(go.Bar(name="Current",  x=compare_df["Channel"], y=compare_df["Current"],  marker_color=COLORS[0]))
    theme(fig, 340); fig.update_layout(barmode="group", bargap=0.3)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    st.markdown(f'<div class="section-card card-orange">{sec_html("Comparison Table","Table","badge-orange","📋")}</div>', unsafe_allow_html=True)
    excel_download(mom, "month_on_month.xlsx")
    st.dataframe(
        mom.style.applymap(style_change, subset=["Change %"]).applymap(style_prev, subset=["Period"]),
        use_container_width=True, height=400
    )

# ======================================================
# SKU DAY-ON-DAY
# ======================================================
elif page == "📦  SKU Day-on-Day":
    st.title("SKU Day-on-Day")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">SKU-level daily sales movement</p>', unsafe_allow_html=True)

    sku_daily = _aggs["sku_daily"].copy()
    sku_daily["Change %"] = ((sku_daily["TotalSales"]-sku_daily["Prev Sales"])/sku_daily["Prev Sales"].replace(0,pd.NA)*100).round(0)
    sku_daily["Change %"] = sku_daily["Change %"].apply(lambda x: f"{int(x)}%" if pd.notna(x) else "")

    top_skus  = _aggs["sku_total"].set_index("SKU")["TotalSales"].nlargest(8).index.tolist()
    chart_skus = st.multiselect("Select SKUs for chart", sorted(df_f["SKU"].unique()), default=top_skus[:5])

    divider()

    st.markdown(f'<div class="section-card card-rose">{sec_html("Daily Trend by SKU","Chart","badge-rose","📈")}</div>', unsafe_allow_html=True)
    chart_df = _aggs["sku_daily"][_aggs["sku_daily"]["SKU"].isin(chart_skus)][["Date","SKU","TotalSales"]].copy()
    fig = px.line(chart_df, x="Date", y="TotalSales", color="SKU",
                  color_discrete_sequence=COLORS,
                  labels={"TotalSales":"Revenue (₹)","Date":""}, markers=True)
    theme(fig, 340)
    fig.update_traces(line=dict(width=2), marker=dict(size=4))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    st.markdown(f'<div class="section-card card-blue">{sec_html("Detailed Data Table","Table","badge-blue","📋")}</div>', unsafe_allow_html=True)
    sku_daily_export = sku_daily.copy()
    sku_daily_export["Date"] = sku_daily_export["Date"].dt.strftime("%Y-%m-%d")
    excel_download(sku_daily_export, "sku_day_on_day.xlsx")
    st.dataframe(sku_daily_export.style.applymap(style_change, subset=["Change %"]),
                 use_container_width=True, height=400)

# ======================================================
# SKU MONTH-ON-MONTH
# ======================================================
elif page == "📊  SKU Month-on-Month":
    st.title("SKU Month-on-Month")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">SKU-level revenue across periods</p>', unsafe_allow_html=True)

    months = sorted(df_f["Month"].unique())
    c1,c2,c3,c4 = st.columns(4)
    prev_month = c1.selectbox("Previous Month (SKU)", months, index=max(0,len(months)-2))
    curr_month = c2.selectbox("Current Month (SKU)",  months, index=len(months)-1)
    start_day  = c3.number_input("Start Day (SKU)", 1, 31, 1)
    end_day    = c4.number_input("End Day (SKU)",   1, 31, 18)

    rows = []
    for sku in sorted(df_f["SKU"].unique()):
        prev_val = curr_val = 0
        for label, month in [("Previous",prev_month),("Current",curr_month)]:
            ms    = pd.to_datetime(f"{month}-01")
            ld    = (ms+pd.offsets.MonthEnd()).day
            s     = ms.replace(day=min(start_day,ld))
            e     = ms.replace(day=min(end_day,ld))
            total = df_f[(df_f["SKU"]==sku)&(df_f["Date"]>=s)&(df_f["Date"]<=e)]["TotalSales"].sum()
            rows.append({"SKU":sku,"Period":label,"Total Sales":int(total),"Change %":""})
            if label=="Previous": prev_val=total
            else: curr_val=total
        if prev_val!=0: rows[-1]["Change %"]=f"{int(((curr_val-prev_val)/prev_val)*100)}%"

    sku_mom   = pd.DataFrame(rows)
    curr_rows  = sku_mom[sku_mom["Period"]=="Current"].copy()
    prev_rows  = sku_mom[sku_mom["Period"]=="Previous"].copy()

    divider()

    st.markdown(f'<div class="section-card card-purple">{sec_html("Top 10 SKU Comparison","Chart","badge-purple","📊")}</div>', unsafe_allow_html=True)
    compare_df = pd.merge(
        prev_rows[["SKU","Total Sales"]].rename(columns={"Total Sales":"Previous"}),
        curr_rows[["SKU","Total Sales"]].rename(columns={"Total Sales":"Current"}),
        on="SKU"
    ).nlargest(10,"Current")
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Previous", x=compare_df["SKU"], y=compare_df["Previous"], marker_color=COLORS[1], opacity=0.7))
    fig.add_trace(go.Bar(name="Current",  x=compare_df["SKU"], y=compare_df["Current"],  marker_color=COLORS[0]))
    theme(fig, 340); fig.update_layout(barmode="group", bargap=0.25)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    st.markdown(f'<div class="section-card card-teal">{sec_html("Full SKU Table","Table","badge-teal","📋")}</div>', unsafe_allow_html=True)
    excel_download(sku_mom, "sku_month_on_month.xlsx")
    st.dataframe(
        sku_mom.style.applymap(style_change, subset=["Change %"]).applymap(style_prev, subset=["Period"]),
        use_container_width=True, height=440
    )

# ======================================================
# TOP SKUs
# ======================================================
elif page == "🏆  Top SKUs":
    st.title("Top SKUs")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Best-performing SKUs by total revenue</p>', unsafe_allow_html=True)

    top_n  = st.slider("Show Top N SKUs", 5, 30, 10)
    top_df = (_aggs["sku_total"].set_index("SKU")["TotalSales"]
              .sort_values(ascending=False).head(top_n).reset_index())
    top_df.columns = ["SKU","Total Sales"]
    top_df["Rank"] = range(1, len(top_df)+1)

    divider()

    st.markdown(f'<div class="section-card card-orange">{sec_html("Revenue Leaderboard","Chart","badge-orange","🏆")}</div>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=top_df["Total Sales"][::-1], y=top_df["SKU"][::-1],
        orientation="h",
        marker=dict(color=top_df["Total Sales"][::-1],
                    colorscale=[[0,"#1e2d50"],[1,"#60a5fa"]],
                    showscale=False, line=dict(width=0)),
        text=[f"₹{v:,}" for v in top_df["Total Sales"][::-1]],
        textposition="outside", textfont=dict(color="#7a90aa",size=10),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>"
    ))
    theme(fig, max(340, top_n*32))
    fig.update_layout(
        xaxis_title="Revenue (₹)", yaxis_title="",
        xaxis=dict(
            tickformat=",.2s", exponentformat="none",
            tickfont=dict(color="#94a3b8", size=11),
            title_font=dict(color="#94a3b8"),
            gridcolor=GRID, linecolor=GRID,
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    st.markdown(f'<div class="section-card card-rose">{sec_html("Rankings Table","Table","badge-rose","📋")}</div>', unsafe_allow_html=True)
    rankings_df = top_df[["Rank","SKU","Total Sales"]].copy()
    excel_download(rankings_df, "top_skus.xlsx")
    st.dataframe(rankings_df, use_container_width=True, height=400)

# ======================================================
# NEW SKUs — Monthly Cohort Tracker (3-month window)
# ======================================================
elif page == "🆕  New SKUs":
    st.title("New SKUs")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Track SKUs that entered for the first time each month — with 3-month cumulative sales window</p>', unsafe_allow_html=True)

    # ── Step 1: Find the very first date each SKU ever appeared (across ALL data, not filtered) ──
    sku_global_first = df.groupby("SKU")["Date"].min().reset_index()
    sku_global_first.columns = ["SKU", "First Date"]
    sku_global_first["First Month"] = sku_global_first["First Date"].dt.to_period("M")

    # ── Step 2: Available months for the selector ──
    all_months_sorted = sorted(sku_global_first["First Month"].unique())
    all_months_str    = [str(m) for m in all_months_sorted]

    if len(all_months_str) < 2:
        st.warning("Not enough months in data to compute new-SKU cohorts.")
        st.stop()

    # ── Step 3: Month selector (default = second month so there's always a "previous") ──
    selected_month_str = st.selectbox(
        "Select Cohort Month  (SKUs that appeared for the FIRST TIME in this month)",
        all_months_str,
        index=1,
        key="new_sku_month_sel",
    )
    selected_period = pd.Period(selected_month_str, freq="M")

    # Months that came BEFORE selected month — a SKU must NOT appear in any of them
    prior_months = [m for m in all_months_sorted if m < selected_period]

    # ── Step 4: Build cohort — SKUs whose first-ever appearance is in selected_month ──
    cohort_skus = sku_global_first[sku_global_first["First Month"] == selected_period]["SKU"].tolist()

    if not cohort_skus:
        st.info(f"No new SKUs found in **{selected_month_str}**. Try a different month.")
        st.stop()

    # ── Step 5: Define the 3-month tracking window ──
    track_start = selected_period.to_timestamp()                        # 1st of cohort month
    track_end   = (selected_period + 3).to_timestamp() - pd.Timedelta(days=1)  # last day of month+2

    # Cap at the latest date available in data
    data_end = df["Date"].max()
    track_end = min(track_end, data_end)

    # Month labels for the 3 tracking months
    track_months = [selected_period + i for i in range(3)]
    track_month_strs = [str(m) for m in track_months]

    # ── Step 6: Build per-SKU summary ──
    cohort_df = df[df["SKU"].isin(cohort_skus)].copy()
    cohort_df["TrMonth"] = cohort_df["Date"].dt.to_period("M")

    rows = []
    for sku in cohort_skus:
        sku_df  = cohort_df[cohort_df["SKU"] == sku]
        first_d = sku_global_first.loc[sku_global_first["SKU"] == sku, "First Date"].iloc[0]

        row = {"SKU": sku, "First Date": first_d.strftime("%Y-%m-%d")}
        total = 0
        for tm in track_months:
            m_sales = int(sku_df[sku_df["TrMonth"] == tm]["TotalSales"].sum())
            row[f"Sales {tm}"] = m_sales
            total += m_sales
        row["Total Sales (3M)"] = total
        rows.append(row)

    result_df = pd.DataFrame(rows).sort_values("Total Sales (3M)", ascending=False)

    # ── Step 7: Metrics ──
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("🆕 New SKUs",         fmt_count(len(result_df)))
    mc2.metric("💰 3-Month Sales",    fmt_num(result_df["Total Sales (3M)"].sum()))
    mc3.metric("📅 Tracking From",    track_start.strftime("%b %Y"))
    mc4.metric("📅 Tracking To",      track_end.strftime("%b %Y"))

    divider()

    # ── Step 8: Bar chart — total 3M sales per SKU (top 20) ──
    st.markdown(f'<div class="section-card card-green">{sec_html(f"New SKU Cohort — {selected_month_str}","3-Month Sales","badge-green","🆕")}</div>', unsafe_allow_html=True)
    chart_df = result_df.head(20)
    fig = go.Figure(go.Bar(
        x=chart_df["Total Sales (3M)"][::-1],
        y=chart_df["SKU"][::-1],
        orientation="h",
        marker=dict(
            color=chart_df["Total Sales (3M)"][::-1],
            colorscale=[[0,"#0e2a1a"],[1,"#34d399"]],
            showscale=False, line=dict(width=0)
        ),
        text=[f"₹{v:,}" for v in chart_df["Total Sales (3M)"][::-1]],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    theme(fig, max(340, len(chart_df) * 34))
    fig.update_layout(
        xaxis_title="3-Month Revenue (₹)", yaxis_title="",
        xaxis=dict(tickformat=",.2s", exponentformat="none",
                   tickfont=dict(color="#94a3b8", size=11),
                   title_font=dict(color="#94a3b8"), gridcolor=GRID, linecolor=GRID),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    divider()

    # ── Step 9: Month-wise stacked bar ──
    st.markdown(f'<div class="section-card card-teal">{sec_html("Month-wise Sales Breakdown","Top 15 SKUs","badge-teal","📊")}</div>', unsafe_allow_html=True)
    top15 = result_df.head(15)
    month_cols = [f"Sales {m}" for m in track_months]
    fig2 = go.Figure()
    bar_colors = ["#60a5fa", "#a78bfa", "#34d399"]
    for i, (mc, tm) in enumerate(zip(month_cols, track_month_strs)):
        fig2.add_trace(go.Bar(
            name=tm,
            x=top15["SKU"],
            y=top15[mc],
            marker_color=bar_colors[i % len(bar_colors)],
            hovertemplate=f"<b>%{{x}}</b><br>{tm}: ₹%{{y:,.0f}}<extra></extra>",
        ))
    fig2.update_layout(barmode="stack")
    theme(fig2, 360)
    fig2.update_traces(marker_line_width=0)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    divider()

    # ── Step 10: Full table ──
    col_order = ["SKU", "First Date"] + [f"Sales {m}" for m in track_months] + ["Total Sales (3M)"]
    display_df = result_df[col_order].copy()
    # Rename month columns to readable labels
    display_df = display_df.rename(columns={f"Sales {m}": f"₹ {m}" for m in track_months})

    st.markdown(f'<div class="section-card card-slate">{sec_html(f"All New SKUs — {selected_month_str} Cohort","Table","badge-blue","📋")}</div>', unsafe_allow_html=True)

    # Highlight note about tracking window
    completed_months = [m for m in track_months if m.to_timestamp() <= data_end]
    pending_months   = [m for m in track_months if m.to_timestamp() > data_end]
    note_parts = []
    if completed_months:
        note_parts.append(f"✅ Completed: {', '.join(str(m) for m in completed_months)}")
    if pending_months:
        note_parts.append(f"⏳ Pending data: {', '.join(str(m) for m in pending_months)}")
    if note_parts:
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748b;margin-bottom:8px;">'
            f'Tracking window: {" &nbsp;|&nbsp; ".join(note_parts)}</div>',
            unsafe_allow_html=True
        )

    excel_download(display_df, f"new_skus_{selected_month_str}.xlsx")
    st.dataframe(display_df, use_container_width=True, height=460)

# ======================================================
# ZERO SALES
# ======================================================
elif page == "⚠️  Zero Sales Alert":
    st.title("Zero Sales Alert")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:22px;font-size:0.9rem;">Dates where a SKU had NO sales — gaps between active selling days</p>', unsafe_allow_html=True)

    # ── Step 1: Daily sales per SKU (sum across channels) ──
    daily_actual = (
        df_f.groupby(["SKU", "Date"])["TotalSales"]
        .sum()
        .reset_index()
    )

    # ── Step 2: For each SKU, build the full date range between its first and last sale ──
    # Any date in that range with no row = zero sales day
    sku_date_range = daily_actual.groupby("SKU")["Date"].agg(["min", "max"]).reset_index()
    sku_date_range.columns = ["SKU", "first_sale", "last_sale"]

    zero_rows = []
    for _, row in sku_date_range.iterrows():
        sku = row["SKU"]
        full_dates = pd.date_range(row["first_sale"], row["last_sale"], freq="D")
        actual_dates = set(daily_actual[daily_actual["SKU"] == sku]["Date"])
        missing = [d for d in full_dates if d not in actual_dates]
        for d in missing:
            zero_rows.append({"SKU": sku, "Date": d, "Total Sales": 0})

    zero_days_df = pd.DataFrame(zero_rows)

    if zero_days_df.empty:
        st.markdown("""
        <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.22);
                    border-radius:16px;padding:48px;text-align:center;margin-top:16px;">
            <div style="font-size:3.5rem;">✅</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.3rem;color:#34d399;
                        margin-top:12px;font-weight:700;">All Clear</div>
            <div style="color:#475569;font-size:0.88rem;margin-top:8px;">
                No missing sales days found for any SKU in the selected period.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        zero_days_df = zero_days_df.sort_values(["SKU", "Date"]).reset_index(drop=True)
        unique_zero_skus = zero_days_df["SKU"].nunique()
        total_zero_days  = len(zero_days_df)

        # ── Metrics ──
        m1, m2 = st.columns(2)
        m1.metric("⚠️ SKUs with gaps",    f"{unique_zero_skus:,}")
        m2.metric("📅 Total missing days", f"{total_zero_days:,}")

        divider()

        # ── Table: SKU | Date | Total Sales ──
        display_df = zero_days_df.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        display_df["Total Sales"] = 0

        st.markdown(f'<div class="section-card card-slate">{sec_html("Zero Sales Days — SKU wise","Table","badge-rose","⚠️")}</div>', unsafe_allow_html=True)
        excel_download(display_df, "zero_sales_gaps.xlsx")
        st.dataframe(display_df, use_container_width=True, height=520)

# ======================================================
# ASK QUESTIONS — AI-powered Q&A on your actual data
# ======================================================
elif page == "🤖  Ask Questions":

    st.title("Ask Questions")
    st.markdown('<p style="color:#475569;margin-top:-8px;margin-bottom:20px;font-size:0.9rem;">Ask anything about your sales data — instant answers from your actual numbers, no API key needed</p>', unsafe_allow_html=True)

    def answer_query(q, df_in):
        import re
        q_low = q.lower()

        def fmts(v):
            if v >= 1e9:  return f"₹{v/1e9:.2f}B"
            if v >= 1e7:  return f"₹{v/1e7:.2f} Cr"
            if v >= 1e5:  return f"₹{v/1e5:.2f}L"
            if v >= 1e3:  return f"₹{v/1e3:.1f}K"
            return f"₹{v:,.0f}"

        def fmtn(v):
            if v >= 1e6: return f"{v/1e6:.2f}M"
            if v >= 1e3: return f"{v/1e3:.1f}K"
            return f"{v:,.0f}"

        months_map = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
                      "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,
                      "january":1,"february":2,"march":3,"april":4,"june":6,
                      "july":7,"august":8,"september":9,"october":10,"november":11,"december":12}

        def df_for_period():
            for m_name, m_num in months_map.items():
                if m_name in q_low:
                    sub = df_in[df_in["Date"].dt.month == m_num]
                    yr_match = re.search(r"\b(20\d{2})\b", q_low)
                    if yr_match:
                        sub = sub[sub["Date"].dt.year == int(yr_match.group(1))]
                    return sub, m_name.capitalize() + (f" {yr_match.group(1)}" if yr_match else "")
            m = re.search(r"last\s+(\d+)\s+day", q_low)
            if m:
                n = int(m.group(1))
                cutoff = df_in["Date"].max() - pd.Timedelta(days=n-1)
                return df_in[df_in["Date"] >= cutoff], f"last {n} days"
            if "last week" in q_low:
                cutoff = df_in["Date"].max() - pd.Timedelta(days=6)
                return df_in[df_in["Date"] >= cutoff], "last 7 days"
            if "last month" in q_low:
                latest = df_in["Date"].max()
                first_this = latest.replace(day=1)
                last_prev  = first_this - pd.Timedelta(days=1)
                first_prev = last_prev.replace(day=1)
                return df_in[(df_in["Date"] >= first_prev) & (df_in["Date"] <= last_prev)], last_prev.strftime("%B %Y")
            m2 = re.search(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})", q)
            if m2:
                try:
                    dt = pd.to_datetime(m2.group(1))
                    sub = df_in[df_in["Date"] == dt]
                    if not sub.empty:
                        return sub, dt.strftime("%d %b %Y")
                except Exception:
                    pass
            return df_in.copy(), "full period"

        d_sub, period_label = df_for_period()
        if d_sub.empty:
            return f"No data found for the requested period."

        def find_sku(text):
            tl = text.lower()
            for sku in sorted(df_in["SKU"].unique(), key=len, reverse=True):
                if sku.lower() in tl:
                    return sku
            return None

        def find_channel(text):
            tl = text.lower()
            for ch in df_in["Channel"].unique():
                if ch.lower() in tl:
                    return ch
            return None

        sku_mentioned = find_sku(q)
        ch_mentioned  = find_channel(q)
        top_m = re.search(r"top\s*(\d+)", q_low)
        top_n = int(top_m.group(1)) if top_m else 5

        # 1. Total sales / cardload / value
        if any(x in q_low for x in ["total sales","total revenue","overall sales","cardload","card load","total value","total card"]):
            ts = int(d_sub["TotalSales"].sum())
            to = int(d_sub["OrderCount"].sum())
            return (f"**Total Sales ({period_label}):** {fmts(ts)}\n\n"
                    f"**Total Orders:** {fmtn(to)}\n\n"
                    f"**Avg Order Value:** {fmts(ts/to) if to else '—'}")

        # 2. Top N SKUs
        if any(x in q_low for x in ["top sku","best sku","highest sku","top product","best product","revenue sku","top 5","top 10"]):
            top = d_sub.groupby("SKU")["TotalSales"].sum().nlargest(top_n).reset_index()
            rows = "\n".join([f"{i+1}. **{r.SKU}** — {fmts(r.TotalSales)}" for i,r in top.iterrows()])
            return f"**Top {top_n} SKUs by Sales ({period_label}):**\n\n{rows}"

        # 3. Specific SKU
        if sku_mentioned:
            sub = d_sub[d_sub["SKU"] == sku_mentioned]
            if sub.empty:
                return f"No data found for **{sku_mentioned}** in the selected period."
            ts = int(sub["TotalSales"].sum())
            to = int(sub["OrderCount"].sum())
            daily_avg = ts / max(sub["Date"].nunique(), 1)
            best_day  = sub.groupby("Date")["TotalSales"].sum().idxmax()
            best_val  = int(sub.groupby("Date")["TotalSales"].sum().max())
            return (f"**{sku_mentioned} ({period_label}):**\n\n"
                    f"- Total Sales: {fmts(ts)}\n"
                    f"- Total Orders: {fmtn(to)}\n"
                    f"- Daily Avg: {fmts(daily_avg)}\n"
                    f"- Best Day: {best_day.strftime('%d %b %Y')} ({fmts(best_val)})")

        # 4. Channel breakdown
        if any(x in q_low for x in ["channel","app vs","web vs","compare channel"]):
            ch_data = d_sub.groupby("Channel").agg(Sales=("TotalSales","sum"), Orders=("OrderCount","sum")).reset_index()
            ch_data = ch_data.sort_values("Sales", ascending=False)
            if ch_mentioned:
                row = ch_data[ch_data["Channel"] == ch_mentioned]
                if not row.empty:
                    r = row.iloc[0]
                    return (f"**{ch_mentioned} ({period_label}):**\n\n"
                            f"- Sales: {fmts(r.Sales)}\n"
                            f"- Orders: {fmtn(r.Orders)}\n"
                            f"- AOV: {fmts(r.Sales/r.Orders) if r.Orders else '—'}")
            rows = "\n".join([f"{i+1}. **{r.Channel}** — {fmts(r.Sales)} ({fmtn(r.Orders)} orders)" for i,r in ch_data.iterrows()])
            top_ch = ch_data.iloc[0]
            return (f"**Channel Breakdown ({period_label}):**\n\n{rows}\n\n"
                    f"🏆 Highest: **{top_ch.Channel}** with {fmts(top_ch.Sales)}")

        # 5. Monthly trend
        if any(x in q_low for x in ["monthly","month trend","month-on-month","mom","by month"]):
            mon = d_sub.groupby("Month")["TotalSales"].sum().reset_index()
            rows = "\n".join([f"- **{r.Month}:** {fmts(r.TotalSales)}" for _,r in mon.iterrows()])
            best = mon.loc[mon["TotalSales"].idxmax()]
            return (f"**Monthly Sales Trend ({period_label}):**\n\n{rows}\n\n"
                    f"📈 Best Month: **{best.Month}** — {fmts(best.TotalSales)}")

        # 6. Daily / best day
        if any(x in q_low for x in ["daily","best day","highest day","day wise","by date"]):
            daily = d_sub.groupby("Date")["TotalSales"].sum().reset_index()
            best  = daily.loc[daily["TotalSales"].idxmax()]
            worst = daily.loc[daily["TotalSales"].idxmin()]
            avg   = daily["TotalSales"].mean()
            return (f"**Daily Sales Summary ({period_label}):**\n\n"
                    f"- Average Daily: {fmts(avg)}\n"
                    f"- Best Day: **{best.Date.strftime('%d %b %Y')}** — {fmts(best.TotalSales)}\n"
                    f"- Lowest Day: **{worst.Date.strftime('%d %b %Y')}** — {fmts(worst.TotalSales)}")

        # 7. Orders
        if any(x in q_low for x in ["order","orders"]):
            to = int(d_sub["OrderCount"].sum())
            ts = int(d_sub["TotalSales"].sum())
            aov = ts // to if to else 0
            top_sku_o = d_sub.groupby("SKU")["OrderCount"].sum().idxmax()
            return (f"**Orders Summary ({period_label}):**\n\n"
                    f"- Total Orders: **{fmtn(to)}**\n"
                    f"- Avg Order Value: {fmts(aov)}\n"
                    f"- Most Ordered SKU: **{top_sku_o}**")

        # 8. Bottom/worst SKUs
        if any(x in q_low for x in ["lowest","worst","least","bottom","poor performing"]):
            bot = d_sub.groupby("SKU")["TotalSales"].sum().nsmallest(top_n).reset_index()
            rows = "\n".join([f"{i+1}. **{r.SKU}** — {fmts(r.TotalSales)}" for i,r in bot.iterrows()])
            return f"**Bottom {top_n} SKUs by Sales ({period_label}):**\n\n{rows}"

        # 9. Summary / overview
        if any(x in q_low for x in ["summary","overview","snapshot","highlight","give me","tell me","what is"]):
            ts   = int(d_sub["TotalSales"].sum())
            to   = int(d_sub["OrderCount"].sum())
            n_sku= d_sub["SKU"].nunique()
            best_ch  = d_sub.groupby("Channel")["TotalSales"].sum().idxmax()
            best_sku = d_sub.groupby("SKU")["TotalSales"].sum().idxmax()
            return (f"**Sales Summary — {period_label}**\n\n"
                    f"- 💰 Total Sales: **{fmts(ts)}**\n"
                    f"- 📦 Total Orders: **{fmtn(to)}**\n"
                    f"- 📈 Avg Order Value: **{fmts(ts/to) if to else '—'}**\n"
                    f"- 🏷️ Active SKUs: **{n_sku}**\n"
                    f"- 🏆 Top Channel: **{best_ch}**\n"
                    f"- 🥇 Top SKU: **{best_sku}**")

        # Fallback
        ts = int(d_sub["TotalSales"].sum())
        to = int(d_sub["OrderCount"].sum())
        return (f"Data for **{period_label}**: Total Sales = **{fmts(ts)}**, Orders = **{fmtn(to)}**.\n\n"
                f"Try: *total sales*, *top 5 SKUs*, *channel breakdown*, *monthly trend*, *best day*, "
                f"*orders summary*, or type a specific SKU name like **Zomato** or **MakeMyTrip**.")

    # ── Chat UI ─────────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    suggestions = [
        "What are the total sales?",
        "Top 5 SKUs by revenue",
        "Channel breakdown",
        "Monthly sales trend",
        "Best selling day",
        "Total orders summary",
    ]
    st.markdown('<div style="font-size:0.72rem;color:#4a6080;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Quick Questions — click to ask</div>', unsafe_allow_html=True)
    qcols = st.columns(3)
    for qi, qtext in enumerate(suggestions):
        if qcols[qi % 3].button(qtext, key=f"sq_{qi}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": qtext})
            st.rerun()

    st.markdown("<hr style='border-color:#1a2236;margin:14px 0;'>", unsafe_allow_html=True)

    # Auto-answer instantly — no API, pure Python
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        user_q = st.session_state.chat_history[-1]["content"]
        answer = answer_query(user_q, df_f)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    # Show chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="display:flex;justify-content:flex-end;margin-bottom:10px;">'
                f'<div style="background:linear-gradient(135deg,#1d4ed8,#6d28d9);color:#fff;'
                f'padding:10px 16px;border-radius:16px 16px 4px 16px;max-width:75%;'
                f'font-size:0.9rem;line-height:1.5;">{msg["content"]}</div></div>',
                unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    c_in, c_btn = st.columns([5, 1])
    with c_in:
        user_input = st.text_input(
            "question", placeholder="e.g. Total sales in March? Top 10 SKUs? MakeMyTrip sales?",
            label_visibility="collapsed", key="qa_input")
    with c_btn:
        if st.button("Send ➤", use_container_width=True, key="qa_send"):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()