import streamlit as st
import os
from datetime import datetime
from parser import parse_cv_with_llm
from expert_system import screen_candidate
from semantic_network import draw_semantic_network
from candidate import Candidate

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="HR Screening Expert System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== PROFESSIONAL CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

    /* ── Base ── */
    html, body, .stApp {
        font-family: 'DM Sans', sans-serif;
        background-color: #F0F2F7;
        color: #1C2333;
    }
    .main .block-container {
        padding: 2rem 2.5rem 4rem;
        max-width: 1280px;
    }

    /* ── Typography ── */
    h1, h2, h3, h4 {
        font-family: 'DM Serif Display', Georgia, serif;
        color: #0D1321;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 2.6rem; line-height: 1.2; }
    h2 { font-size: 1.8rem; }
    h3 { font-size: 1.3rem; }

    /* ── Page Header ── */
    .page-header {
        background: linear-gradient(135deg, #0D1321 0%, #1a2744 50%, #0f3460 100%);
        border-radius: 20px;
        padding: 40px 48px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(13, 19, 33, 0.25);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 280px; height: 280px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    }
    .page-header::after {
        content: '';
        position: absolute;
        bottom: -80px; left: 30%;
        width: 350px; height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,0.09) 0%, transparent 70%);
    }
    .page-header h1 {
        color: #ffffff;
        margin: 0 0 8px;
        font-size: 2.4rem;
        position: relative;
        z-index: 1;
    }
    .page-header p {
        color: rgba(255,255,255,0.65);
        font-size: 1rem;
        margin: 0;
        font-weight: 300;
        letter-spacing: 0.01em;
        position: relative;
        z-index: 1;
    }
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        color: rgba(255,255,255,0.8);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 14px;
        position: relative;
        z-index: 1;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0D1321 !important;
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.85) !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] strong {
        color: #ffffff !important;
        font-family: 'DM Serif Display', serif;
    }
    [data-testid="stSidebar"] .stMarkdown hr {
        border-color: rgba(255,255,255,0.1) !important;
    }
    .sidebar-tag {
        background: rgba(99,179,237,0.15);
        border: 1px solid rgba(99,179,237,0.25);
        color: #93c5fd !important;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.82rem;
        display: block;
        margin: 6px 0;
        font-weight: 500;
    }
    .sidebar-presenter {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 8px;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 14px;
        padding: 6px;
        gap: 4px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 0.9rem;
        color: #64748b;
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #0f172a;
    }
    .stTabs [aria-selected="true"] {
        background: #0D1321 !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ── Cards ── */
    .card {
        background: white;
        border-radius: 18px;
        padding: 28px 32px;
        border: 1px solid #e8ecf4;
        box-shadow: 0 4px 20px rgba(13,19,33,0.06);
        transition: box-shadow 0.2s ease;
    }
    .card:hover { box-shadow: 0 8px 32px rgba(13,19,33,0.1); }

    .card-sm {
        background: white;
        border-radius: 14px;
        padding: 20px 24px;
        border: 1px solid #e8ecf4;
        box-shadow: 0 2px 12px rgba(13,19,33,0.05);
    }

    /* ── Verdict Banners ── */
    .verdict-qualified {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 28px 32px;
        border-radius: 18px;
        border-left: 6px solid #059669;
        box-shadow: 0 8px 32px rgba(5, 150, 105, 0.12);
        margin-bottom: 24px;
    }
    .verdict-qualified .verdict-label {
        color: #065f46;
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        margin: 0;
    }
    .verdict-qualified .verdict-sub {
        color: #047857;
        font-size: 0.9rem;
        margin: 4px 0 0;
    }

    .verdict-hold {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 28px 32px;
        border-radius: 18px;
        border-left: 6px solid #d97706;
        box-shadow: 0 8px 32px rgba(217, 119, 6, 0.12);
        margin-bottom: 24px;
    }
    .verdict-hold .verdict-label {
        color: #78350f;
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        margin: 0;
    }
    .verdict-hold .verdict-sub {
        color: #92400e;
        font-size: 0.9rem;
        margin: 4px 0 0;
    }

    .verdict-rejected {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        padding: 28px 32px;
        border-radius: 18px;
        border-left: 6px solid #e11d48;
        box-shadow: 0 8px 32px rgba(225, 29, 72, 0.12);
        margin-bottom: 24px;
    }
    .verdict-rejected .verdict-label {
        color: #881337;
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        margin: 0;
    }
    .verdict-rejected .verdict-sub {
        color: #9f1239;
        font-size: 0.9rem;
        margin: 4px 0 0;
    }

    /* ── Reasoning Trace ── */
    .trace-step {
        padding: 18px 22px;
        background: white;
        border-radius: 14px;
        margin: 12px 0;
        border-left: 5px solid #6366f1;
        box-shadow: 0 3px 14px rgba(99,102,241,0.08);
        border: 1px solid #e0e7ff;
        border-left: 5px solid #6366f1;
    }
    .trace-step .rule-id {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 9px;
        border-radius: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .trace-step .rule-name {
        font-weight: 600;
        color: #1e293b;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .trace-step .rule-explanation {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ── Knowledge Base Rules ── */
    .rule-card {
        background: white;
        padding: 18px 22px;
        border-radius: 14px;
        margin-bottom: 10px;
        border: 1px solid #e8ecf4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        gap: 16px;
        transition: box-shadow 0.15s ease;
    }
    .rule-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
    .rule-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .rule-id-pill {
        font-size: 0.78rem;
        font-weight: 700;
        background: #f1f5f9;
        color: #475569;
        padding: 3px 10px;
        border-radius: 6px;
        flex-shrink: 0;
        letter-spacing: 0.03em;
    }
    .rule-info { flex: 1; }
    .rule-name-text {
        font-weight: 600;
        font-size: 0.93rem;
        color: #1e293b;
    }
    .rule-desc-text {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 2px;
    }
    .rule-verdict-pill {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        flex-shrink: 0;
        letter-spacing: 0.03em;
    }

    /* ── Section titles ── */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-bottom: 12px;
    }

    /* ── Upload area ── */
    [data-testid="stFileUploadDropzone"] {
        background: white !important;
        border: 2px dashed #c7d2fe !important;
        border-radius: 16px !important;
        transition: border-color 0.2s ease, background 0.2s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #818cf8 !important;
        background: #f5f3ff !important;
    }

    /* ── Buttons ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0D1321, #1e3a5f) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em;
        box-shadow: 0 4px 14px rgba(13,19,33,0.2) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(13,19,33,0.28) !important;
    }
    .stButton > button[kind="secondary"] {
        border-radius: 10px !important;
        font-weight: 500 !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 18px 22px;
        border: 1px solid #e8ecf4;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricLabel"] { font-size: 0.82rem; color: #64748b; font-weight: 500; }
    [data-testid="stMetricValue"] { font-family: 'DM Serif Display', serif; font-size: 1.9rem; color: #0D1321; }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #818cf8) !important;
        border-radius: 99px;
    }
    .stProgress > div {
        background: #e8ecf4 !important;
        border-radius: 99px;
        height: 8px !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

    /* ── Info / success / error boxes ── */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ── Divider ── */
    hr { border-color: #e8ecf4 !important; }

    /* ── Screening wrapper ── */
    .screening-shell {
        max-width: 760px;
        margin: 0 auto;
    }

    /* ── Progress header ── */
    .progress-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .progress-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6366f1;
    }
    .progress-fraction {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94a3b8;
        background: #f1f5f9;
        padding: 3px 10px;
        border-radius: 20px;
    }

    /* ── Question card ── */
    .question-card {
        background: white;
        border-radius: 22px;
        padding: 44px 48px 36px;
        border: 1px solid #e2e8f4;
        box-shadow: 0 8px 40px rgba(13,19,33,0.09), 0 1px 3px rgba(13,19,33,0.04);
        position: relative;
        overflow: hidden;
        margin-top: 20px;
    }
    .question-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #818cf8, #a5b4fc);
        border-radius: 22px 22px 0 0;
    }
    .question-card::after {
        content: '';
        position: absolute;
        top: -80px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,0.05) 0%, transparent 70%);
        pointer-events: none;
    }
    .question-number {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6366f1;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .question-number::before {
        content: '';
        display: inline-block;
        width: 6px; height: 6px;
        background: #6366f1;
        border-radius: 50%;
    }
    .question-text {
        font-family: 'DM Serif Display', serif;
        font-size: 1.55rem;
        color: #0D1321;
        line-height: 1.45;
        margin-bottom: 0;
        position: relative;
        z-index: 1;
    }

    /* ── Answer options ── */
    .answer-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 32px;
    }
    .answer-option {
        display: flex;
        align-items: center;
        gap: 14px;
        background: #fafbfc;
        border: 1.5px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 20px;
        cursor: pointer;
        transition: all 0.18s ease;
        position: relative;
        overflow: hidden;
    }
    .answer-option:hover {
        border-color: #818cf8;
        background: #f5f3ff;
        box-shadow: 0 4px 18px rgba(99,102,241,0.1);
        transform: translateY(-1px);
    }
    .answer-option.selected {
        border-color: #6366f1;
        background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
        box-shadow: 0 4px 20px rgba(99,102,241,0.15);
    }
    .answer-option .option-indicator {
        width: 22px; height: 22px;
        border-radius: 50%;
        border: 2px solid #cbd5e1;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
        transition: all 0.18s ease;
        background: white;
    }
    .answer-option.selected .option-indicator {
        border-color: #6366f1;
        background: #6366f1;
    }
    .answer-option.selected .option-indicator::after {
        content: '';
        display: block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: white;
    }
    .answer-option .option-letter {
        font-size: 0.72rem;
        font-weight: 800;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        flex-shrink: 0;
        width: 18px;
        transition: color 0.18s ease;
    }
    .answer-option.selected .option-letter { color: #6366f1; }
    .answer-option .option-text {
        font-size: 0.95rem;
        font-weight: 500;
        color: #1e293b;
        line-height: 1.4;
        flex: 1;
    }
    .answer-option.selected .option-text {
        color: #3730a3;
        font-weight: 600;
    }

    /* ── Nav row ── */
    .nav-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 32px;
        padding-top: 24px;
        border-top: 1px solid #f1f5f9;
    }

    /* ── Answered chips ── */
    .answered-summary {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    .answered-chip {
        width: 28px; height: 28px;
        border-radius: 8px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 0.72rem; font-weight: 700;
        border: 1.5px solid;
    }
    .answered-chip.done {
        background: #eef2ff; border-color: #818cf8; color: #4f46e5;
    }
    .answered-chip.current {
        background: #6366f1; border-color: #6366f1; color: white;
    }
    .answered-chip.todo {
        background: #f8fafc; border-color: #e2e8f0; color: #94a3b8;
    }

    /* ── Profile grid ── */
    .profile-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .profile-item:last-child { border-bottom: none; }
    .profile-key {
        font-size: 0.84rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .profile-val {
        font-size: 0.92rem;
        color: #1e293b;
        font-weight: 600;
    }

    /* ── Score row ── */
    .score-row {
        margin-bottom: 16px;
    }
    .score-row-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    .score-label { font-size: 0.85rem; font-weight: 600; color: #334155; }
    .score-pts { font-size: 0.82rem; color: #94a3b8; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "history" not in st.session_state:
    st.session_state.history = []
if "screened" not in st.session_state:
    st.session_state.screened = None
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.markdown("### HR Screening")
    st.markdown("<p style='color:rgba(255,255,255,0.5); font-size:0.85rem; margin-top:-8px;'>AI Expert System</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.82rem;'>Intelligent CV Filtering & Candidate Triage</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p class='section-label' style='color:rgba(255,255,255,0.35);'>Knowledge Representation</p>", unsafe_allow_html=True)
    for tag in ["Production Rules", "Forward Chaining", "Frames", "Semantic Networks"]:
        st.markdown(f'<span class="sidebar-tag">⬡ {tag}</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div class="sidebar-presenter">
        <p style="font-size:0.75rem; color:rgba(255,255,255,0.35); margin:0 0 4px; text-transform:uppercase; letter-spacing:0.07em;">Presented to</p>
        <p style="font-size:0.88rem; color:rgba(255,255,255,0.85); margin:0; font-weight:600;">Prof. Dr. Mohamed Roshdy</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("""
<div class="page-header">
    <div class="header-badge">⬡ Classical AI · Knowledge Representation</div>
    <h1>HR Screening Expert System</h1>
    <p>Automating Recruitment Decisions with Production Rules, Forward Chaining & Semantic Networks</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Upload CV",
    "🎯 Start Screening",
    "📊 Screening Result",
    "📈 Dashboard",
    "🌐 Semantic Network",
    "📚 Knowledge Base"
])

# ── Shared helper: render verdict banner ──────────────────────────────────────
def render_verdict(screened):
    if screened.status == "QUALIFIED":
        st.markdown("""
        <div class="verdict-qualified">
            <p class="verdict-label">🎉 Qualified Candidate</p>
            <p class="verdict-sub">This candidate meets the criteria and is recommended for the next stage.</p>
        </div>""", unsafe_allow_html=True)
    elif screened.status == "HOLD":
        st.markdown("""
        <div class="verdict-hold">
            <p class="verdict-label">⏳ On Hold — Talent Pool</p>
            <p class="verdict-sub">Candidate shows potential but doesn't fully meet current requirements.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="verdict-rejected">
            <p class="verdict-label">✕ Rejected</p>
            <p class="verdict-sub">Candidate does not meet the minimum qualifications for this role.</p>
        </div>""", unsafe_allow_html=True)

# ── Shared helper: render profile + score breakdown + trace ──────────────────
def render_result_detail(screened):
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="section-label">Candidate Profile</p>', unsafe_allow_html=True)
        profile_data = {
            "Name": screened.name,
            "Experience": f"{screened.years_experience:.1f} years",
            "Degree": screened.degree_level,
            "Field of Study": screened.field_of_study,
        }
        items_html = "".join(
            f'<div class="profile-item"><span class="profile-key">{k}</span><span class="profile-val">{v}</span></div>'
            for k, v in profile_data.items()
        )
        st.markdown(f'<div class="card-sm">{items_html}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-label">Score Breakdown</p>', unsafe_allow_html=True)
        if screened.score_breakdown:
            rows_html = ""
            for k, v in screened.score_breakdown.items():
                if k != "total":
                    label = k.replace("_", " ").title()
                    max_val = 30 if k == "experience" else 25 if k in ["education", "tech_skills"] else 10
                    percent = min(100, int((v / max_val) * 100))
                    rows_html += f"""
                    <div class="score-row">
                        <div class="score-row-header">
                            <span class="score-label">{label}</span>
                            <span class="score-pts">{v} / {max_val} pts</span>
                        </div>
                        <div style="height:8px;background:#e8ecf4;border-radius:99px;overflow:hidden;">
                            <div style="height:100%;width:{percent}%;background:linear-gradient(90deg,#6366f1,#818cf8);border-radius:99px;transition:width 0.6s ease;"></div>
                        </div>
                    </div>"""
            st.markdown(f'<div class="card-sm">{rows_html}</div>', unsafe_allow_html=True)

    # Reasoning trace
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">⚡ Forward Chaining — Reasoning Trace</p>', unsafe_allow_html=True)
    for step in screened.reasoning_trace:
        if step.get("type") == "FIRE":
            st.markdown(f"""
            <div class="trace-step">
                <div class="rule-id">{step.get('rule_id', '')}</div>
                <div class="rule-name">{step.get('rule_name', '')}</div>
                <div class="rule-explanation">{step.get('explanation', '')}</div>
            </div>
            """, unsafe_allow_html=True)

# ====================== TAB 1: UPLOAD CV ======================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    col_upload, col_info = st.columns([3, 2], gap="large")

    with col_upload:
        st.markdown('<p class="section-label">Upload Candidate Resumes</p>', unsafe_allow_html=True)

        # ── Multi-file uploader ──────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload one or more PDF CVs",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # File queue preview
        if uploaded_files:
            st.markdown("<br>", unsafe_allow_html=True)
            verdict_icon = {"QUALIFIED": "✅", "HOLD": "⏳", "REJECTED": "✕"}
            verdict_color = {"QUALIFIED": "#059669", "HOLD": "#d97706", "REJECTED": "#e11d48"}

            # Summary badge row
            count = len(uploaded_files)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <div style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:10px;
                            padding:8px 18px;font-size:0.88rem;font-weight:600;color:#4f46e5;">
                    {count} CV{'s' if count > 1 else ''} queued
                </div>
                <div style="font-size:0.82rem;color:#94a3b8;">
                    Each will be parsed and screened individually
                </div>
            </div>
            """, unsafe_allow_html=True)

            # File list preview cards
            for uf in uploaded_files:
                ext = uf.name.split(".")[-1].upper()
                size_kb = round(uf.size / 1024, 1)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:14px;background:white;
                            border:1px solid #e8ecf4;border-radius:12px;padding:12px 18px;
                            margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,0.04);">
                    <div style="width:38px;height:38px;background:#f1f5f9;border-radius:9px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:0.72rem;font-weight:800;color:#475569;letter-spacing:0.03em;">
                        {ext}
                    </div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-size:0.9rem;font-weight:600;color:#1e293b;
                                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                            {uf.name}
                        </div>
                        <div style="font-size:0.78rem;color:#94a3b8;margin-top:2px;">{size_kb} KB</div>
                    </div>
                    <div style="font-size:0.75rem;font-weight:600;color:#6366f1;background:#eef2ff;
                                padding:3px 10px;border-radius:20px;">Ready</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            btn_label = f"🚀 Screen {count} Candidate{'s' if count > 1 else ''}"
            if st.button(btn_label, type="primary", use_container_width=True):
                batch_results = []
                progress_bar = st.progress(0, text="Initialising…")

                for i, uf in enumerate(uploaded_files):
                    progress_bar.progress(
                        (i) / count,
                        text=f"Processing {i+1}/{count}: {uf.name}"
                    )

                    # Determine extension and write temp file
                    ext_lower = uf.name.rsplit(".", 1)[-1].lower()
                    temp_path = f"temp_cv_{i}.{ext_lower}"
                    with open(temp_path, "wb") as f:
                        f.write(uf.getbuffer())

                    try:
                        candidate = parse_cv_with_llm(temp_path)
                        screened = screen_candidate(candidate)
                    except Exception as e:
                        screened = Candidate(name=uf.name, status="REJECTED", confidence=0.0)
                        screened.explanation = [f"Parse error: {str(e)}"]
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                    batch_results.append((uf.name, screened))

                    st.session_state.screened = screened  # keep last as "most recent"
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "name": screened.name,
                        "verdict": screened.status,
                        "score": round(screened.confidence * 100, 1),
                        "rule": screened.fired_rules[0]["rule"] if screened.fired_rules else "N/A",
                        "source": f"CV Upload ({uf.name})"
                    })

                progress_bar.progress(1.0, text="All CVs processed!")

                # ── Batch summary bar ────────────────────────────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                n_qual = sum(1 for _, s in batch_results if s.status == "QUALIFIED")
                n_hold = sum(1 for _, s in batch_results if s.status == "HOLD")
                n_rej  = sum(1 for _, s in batch_results if s.status == "REJECTED")

                st.markdown(f"""
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:28px;">
                    <div style="background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-radius:14px;
                                padding:18px 22px;border-left:4px solid #059669;text-align:center;">
                        <div style="font-size:1.9rem;font-weight:800;color:#065f46;font-family:'DM Serif Display',serif;">{n_qual}</div>
                        <div style="font-size:0.8rem;font-weight:600;color:#047857;text-transform:uppercase;letter-spacing:0.07em;">Qualified</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:14px;
                                padding:18px 22px;border-left:4px solid #d97706;text-align:center;">
                        <div style="font-size:1.9rem;font-weight:800;color:#78350f;font-family:'DM Serif Display',serif;">{n_hold}</div>
                        <div style="font-size:0.8rem;font-weight:600;color:#92400e;text-transform:uppercase;letter-spacing:0.07em;">On Hold</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#fff1f2,#ffe4e6);border-radius:14px;
                                padding:18px 22px;border-left:4px solid #e11d48;text-align:center;">
                        <div style="font-size:1.9rem;font-weight:800;color:#881337;font-family:'DM Serif Display',serif;">{n_rej}</div>
                        <div style="font-size:0.8rem;font-weight:600;color:#9f1239;text-transform:uppercase;letter-spacing:0.07em;">Rejected</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Per-candidate result accordion ───────────────────────────
                st.markdown('<p class="section-label">Individual Results</p>', unsafe_allow_html=True)

                for filename, screened in batch_results:
                    vdict = {
                        "QUALIFIED": ("#059669", "#ecfdf5", "#065f46", "✅ Qualified"),
                        "HOLD":      ("#d97706", "#fffbeb", "#78350f", "⏳ On Hold"),
                        "REJECTED":  ("#e11d48", "#fff1f2", "#881337", "✕ Rejected"),
                    }
                    border_c, bg_c, text_c, label = vdict.get(
                        screened.status, ("#6366f1", "#eef2ff", "#3730a3", "? Unknown")
                    )
                    score_pct = round(screened.confidence * 100, 1)

                    with st.expander(f"{label}  ·  {screened.name}  ·  {score_pct}%  —  {filename}"):
                        render_verdict(screened)
                        st.metric("Qualification Score", f"{score_pct}%")
                        render_result_detail(screened)

# ====================== TAB 2: START SCREENING ======================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
        st.session_state.answers = {}

    QUESTIONS = [
        {"id": "experience", "text": "How many years of professional experience does the candidate have?",
         "options": ["Less than 1 year", "1 - 2 years", "3 - 4 years", "5+ years"]},
        {"id": "degree", "text": "What is the candidate's highest education level?",
         "options": ["Bachelor's Degree", "Master's Degree", "PhD", "No University Degree"]},
        {"id": "field_related", "text": "Is the field of study related to the job?",
         "options": ["Yes - Strongly Related", "Yes - Moderately Related", "No - Unrelated"]},
        {"id": "tech_skills", "text": "What is the candidate's technical skill level?",
         "options": ["Beginner (Level 1)", "Intermediate (Level 2)", "Advanced (Level 3)", "Expert (Level 4)"]},
        {"id": "soft_skills", "text": "How strong are the candidate's soft skills?",
         "options": ["Weak", "Average", "Strong", "Excellent"]},
        {"id": "high_potential", "text": "Does the candidate show high learning potential or strong projects?",
         "options": ["Yes - Very Strong", "Yes - Moderate", "No"]},
        {"id": "certifications", "text": "How many relevant certifications does the candidate have?",
         "options": ["None", "1-2", "3 or more"]},
        {"id": "references", "text": "Does the candidate have good professional references?",
         "options": ["Yes", "No", "Not mentioned"]},
        {"id": "location", "text": "Is the candidate's location acceptable?",
         "options": ["Yes", "No"]}
    ]

    q = QUESTIONS[st.session_state.current_q]
    total_q = len(QUESTIONS)
    current_idx = st.session_state.current_q
    progress_pct = (current_idx + 1) / total_q

    # ── Centered screening shell ────────────────────────────────────────────────
    _, center_col, _ = st.columns([1, 5, 1])
    with center_col:

        # Step tracker chips
        chips_html = '<div class="answered-summary">'
        for i in range(total_q):
            if i < current_idx:
                chips_html += f'<div class="answered-chip done">{i+1}</div>'
            elif i == current_idx:
                chips_html += f'<div class="answered-chip current">{i+1}</div>'
            else:
                chips_html += f'<div class="answered-chip todo">{i+1}</div>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div class="progress-header" style="margin-top:14px;">
            <span class="progress-label">Screening Progress</span>
            <span class="progress-fraction">{current_idx + 1} of {total_q} questions</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_pct)

        # Question card
        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">Question {current_idx + 1} &nbsp;·&nbsp; {q['id'].replace('_', ' ').title()}</div>
            <div class="question-text">{q['text']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Answer options — rendered as styled HTML labels + hidden Streamlit radio for state
        letters = ["A", "B", "C", "D"]
        current_val = st.session_state.get(f"q_{current_idx}", q['options'][0])

        options_html = '<div class="answer-grid">'
        for i, opt in enumerate(q['options']):
            is_selected = (current_val == opt)
            selected_cls = "selected" if is_selected else ""
            options_html += f"""
            <div class="answer-option {selected_cls}">
                <div class="option-indicator"></div>
                <span class="option-letter">{letters[i] if i < len(letters) else str(i+1)}</span>
                <span class="option-text">{opt}</span>
            </div>"""
        options_html += '</div>'
        st.markdown(options_html, unsafe_allow_html=True)

        # Actual radio (hidden label, drives state)
        st.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
        choice = st.radio(
            "Choose your answer:",
            q['options'],
            key=f"q_{current_idx}",
            label_visibility="collapsed",
            horizontal=len(q['options']) <= 4
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Navigation row
        nav_left, nav_right = st.columns([1, 2])
        with nav_left:
            if st.button("← Back", disabled=(current_idx == 0), use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()

        with nav_right:
            is_last = current_idx == total_q - 1
            btn_label = "Run Inference Engine →" if is_last else "Next Question →"
            if st.button(btn_label, type="primary", use_container_width=True):
                st.session_state.answers[q['id']] = choice

                if not is_last:
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    with st.spinner("Running Forward Chaining Inference Engine…"):
                        exp_map = {"Less than 1 year": 0.5, "1 - 2 years": 1.5, "3 - 4 years": 3.5, "5+ years": 6}
                        exp_years = exp_map.get(st.session_state.answers.get("experience"), 0)

                        degree_str = st.session_state.answers.get("degree", "")
                        has_degree = "Bachelor" in degree_str or "Master" in degree_str or "PhD" in degree_str
                        field_related = "Related" in st.session_state.answers.get("field_related", "")

                        tech_str = st.session_state.answers.get("tech_skills", "")
                        tech_level = int(''.join(filter(str.isdigit, tech_str))) if any(c.isdigit() for c in tech_str) else 2

                        high_potential = "Very Strong" in st.session_state.answers.get("high_potential", "")

                        dummy_candidate = Candidate(
                            name="Interactive Candidate",
                            years_experience=exp_years,
                            degree_level="Bachelor" if has_degree else "None",
                            field_of_study="Computer Science" if field_related else "Other",
                            technical_skills=["Python", "SQL"],
                            has_demonstrated_potential=high_potential
                        )

                        screened = screen_candidate(dummy_candidate)
                        st.session_state.screened = screened

                        st.session_state.history.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "name": screened.name,
                            "verdict": screened.status,
                            "score": round(screened.confidence * 100, 1),
                            "rule": screened.fired_rules[0]["rule"] if screened.fired_rules else "N/A",
                            "source": "Interactive Screening"
                        })

                    st.success("✅ Screening completed successfully!")
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<p class="section-label">Screening Result</p>', unsafe_allow_html=True)
                    render_verdict(screened)
                    st.metric("Overall Score", f"{screened.confidence*100:.1f}%")
                    render_result_detail(screened)

# ====================== TAB 3: SCREENING RESULT ======================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.screened:
        screened = st.session_state.screened
        st.markdown('<p class="section-label">Most Recent Screening Result</p>', unsafe_allow_html=True)
        render_verdict(screened)
        st.metric("Overall Qualification Score", f"{screened.confidence*100:.1f}%")
        render_result_detail(screened)
    else:
        st.info("No screening has been run yet. Use **Upload CV** or **Start Screening** to begin.")

# ====================== TAB 4: DASHBOARD ======================
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Screening History & Analytics</p>', unsafe_allow_html=True)

    if st.session_state.history:
        qualified = len([h for h in st.session_state.history if h["verdict"] == "QUALIFIED"])
        on_hold   = len([h for h in st.session_state.history if h["verdict"] == "HOLD"])
        rejected  = len([h for h in st.session_state.history if h["verdict"] == "REJECTED"])
        total     = len(st.session_state.history)

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Total Screened", total)
        with m2: st.metric("✅ Qualified", qualified)
        with m3: st.metric("⏳ On Hold", on_hold)
        with m4: st.metric("✕ Rejected", rejected)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(st.session_state.history, use_container_width=True)
    else:
        st.info("No screening history yet. Screen candidates to populate the dashboard.")

# ====================== TAB 5: SEMANTIC NETWORK ======================
with tab5:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Semantic Network Visualization</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-sm" style="margin-bottom:20px;">
        <p style="color:#475569;font-size:0.9rem;margin:0;line-height:1.6;">
            The semantic network represents relationships between candidate attributes, rules, and verdicts
            using nodes and typed edges — a core knowledge representation technique.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Show Semantic Network Visualization", type="primary"):
        draw_semantic_network()
        st.success("Semantic Network opened in a new window.")

# ====================== TAB 6: KNOWLEDGE BASE ======================
with tab6:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Production Rules — Knowledge Base</p>', unsafe_allow_html=True)

    rules = [
        ("R1", "Ideal Match",              "Qualified", "≥3 years + Related Degree + Strong Tech Skills"),
        ("R2", "Senior Expert",            "Qualified", "≥5 years experience"),
        ("R3", "Rising Star",              "Hold",      "High-potential fresh graduate"),
        ("R4", "Skilled But Inexperienced","Hold",      "Strong skills with limited experience"),
        ("R5", "Skills Gap",               "Rejected",  "Insufficient technical skills"),
        ("R6", "Entry Level",              "Rejected",  "Less than 1 year experience"),
        ("R7", "Education Mismatch",       "Rejected",  "No degree + unrelated field"),
    ]

    verdict_styles = {
        "Qualified": ("#059669", "#d1fae5", "#065f46"),
        "Hold":      ("#d97706", "#fef3c7", "#78350f"),
        "Rejected":  ("#e11d48", "#ffe4e6", "#881337"),
    }

    for rid, name, cat, desc in rules:
        dot_color, pill_bg, pill_text = verdict_styles[cat]
        st.markdown(f"""
        <div class="rule-card">
            <div class="rule-dot" style="background:{dot_color};"></div>
            <div class="rule-id-pill">{rid}</div>
            <div class="rule-info">
                <div class="rule-name-text">{name}</div>
                <div class="rule-desc-text">{desc}</div>
            </div>
            <div class="rule-verdict-pill" style="background:{pill_bg};color:{pill_text};">{cat}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:20px 0;border-top:1px solid #e2e8f0;">
    <p style="color:#94a3b8;font-size:0.8rem;margin:0;">
        HR Screening Expert System &nbsp;·&nbsp; Knowledge Representation Techniques &nbsp;·&nbsp; Prof. Dr. Mohamed Roshdy
    </p>
</div>
""", unsafe_allow_html=True)