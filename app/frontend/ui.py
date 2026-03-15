import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroAgent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #070710 !important;
    font-family: 'DM Sans', sans-serif;
    color: #e8e8f0;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 2rem 2rem 0 2rem !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Background grid */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* Glow orb */
.stApp::after {
    content: '';
    position: fixed;
    width: 700px; height: 700px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.07) 0%, transparent 70%);
    top: -150px; right: -150px;
    pointer-events: none;
    z-index: 0;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* ── Navbar ── */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0 1.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    background: linear-gradient(135deg, #a5b4fc, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.nav-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    color: #a5b4fc;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Layout ── */
.layout {
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 2rem;
    position: relative;
    z-index: 1;
}

/* ── Sidebar ── */
.sidebar-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(232,232,240,0.3);
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}
.sidebar-label:first-child { margin-top: 0; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    padding: 0.7rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    background: rgba(99,102,241,0.04) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
    outline: none !important;
}
.stTextInput label {
    color: rgba(232,232,240,0.5) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Textarea ── */
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    resize: vertical !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
    outline: none !important;
}
.stTextArea label {
    color: rgba(232,232,240,0.5) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
}
.stSelectbox label {
    color: rgba(232,232,240,0.5) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    color: rgba(232,232,240,0.65) !important;
    font-size: 0.9rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Section title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #e8e8f0;
    margin-bottom: 0.25rem;
    line-height: 1.2;
}
.section-sub {
    color: rgba(232,232,240,0.35);
    font-size: 0.85rem;
    margin-bottom: 2rem;
    letter-spacing: 0.3px;
}

/* ── Divider ── */
.thin-divider {
    height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

/* ── Response ── */
.response-wrap {
    margin-top: 2rem;
    background: rgba(99,102,241,0.04);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 18px;
    padding: 1.75rem 2rem;
    position: relative;
}
.response-tag {
    position: absolute;
    top: -11px;
    left: 20px;
    background: #070710;
    padding: 0 10px;
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #818cf8;
}
.response-body {
    color: #d1d5db;
    line-height: 1.85;
    font-size: 0.95rem;
    white-space: pre-wrap;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 3rem 0 1.5rem;
    color: rgba(232,232,240,0.15);
    font-size: 0.72rem;
    font-family: 'Syne', sans-serif;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)

# ── Navbar ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">⚡ NeuroAgent</div>
    <div class="nav-badge">🟢 Online</div>
</div>
""", unsafe_allow_html=True)

# ── Layout: Sidebar + Main ─────────────────────────────────────────────────────
sidebar_col, main_col = st.columns([1, 3])

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with sidebar_col:
    st.markdown('<div class="sidebar-label">🤖 AI Engine</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Model",
        settings.ALLOWED_MODEL_NAMES,
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-label">🌐 Web Search</div>', unsafe_allow_html=True)
    allow_search = st.checkbox("Enable Tavily Search", value=False)

    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
    border-radius:12px;padding:1rem;font-size:0.8rem;color:rgba(232,232,240,0.4);line-height:1.6;">
        💡 <strong style="color:rgba(232,232,240,0.6)">Tip:</strong><br>
        Define a clear system prompt like<br>
        <em>"You are a Python expert"</em><br>
        for precise results.
    </div>
    """, unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
with main_col:
    st.markdown("""
    <div class="section-title">AI Agent Studio</div>
    <div class="section-sub">LangGraph · Groq · Tavily — Real-time Intelligence</div>
    """, unsafe_allow_html=True)

    system_prompt = st.text_area(
        "Agent Persona (System Prompt)",
        height=95,
        placeholder="e.g. You are a Senior Financial Analyst with expertise in global markets...",
        value="You are a helpful AI assistant."
    )

    user_query = st.text_area(
        "Your Query",
        height=130,
        placeholder="Ask anything... What are the top AI trends in 2025?"
    )

    API_URL = "http://127.0.0.1:9999/chat"

    if st.button("⚡  Generate Response"):
        if not user_query.strip():
            st.warning("Please enter a query first.")
        else:
            payload = {
                "model_name"   : selected_model,
                "system_prompt": system_prompt,
                "messages"     : [user_query],
                "allow_message": allow_search,
            }
            with st.spinner("Agent is thinking..."):
                try:
                    logger.info("Sending request to backend...")
                    res = requests.post(API_URL, json=payload, timeout=60)

                    if res.status_code == 200:
                        agent_response = res.json().get("response", "")
                        logger.info("Response received.")
                        st.markdown(f"""
                        <div class="response-wrap">
                            <div class="response-tag">⚡ Agent Response</div>
                            <div class="response-body">{agent_response}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Error {res.status_code}: {res.json().get('detail', 'Something went wrong.')}")

                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">NeuroAgent · Built with LangGraph & Groq · LLMOps</div>
""", unsafe_allow_html=True)