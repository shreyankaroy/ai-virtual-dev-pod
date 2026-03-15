"""
AI-Powered Virtual Development Pod — Streamlit Dashboard
Run with: streamlit run frontend/streamlit_app.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Virtual Dev Pod",
    page_icon="🤖",
    layout="wide",
)

# ─────────────────────────────────────────────
# Custom UI Styling
# ─────────────────────────────────────────────

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg,#0f172a,#020617);
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #e2e8f0;
}

.stTextArea textarea {
    background: #020617;
    color: white;
}

.stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    color:white;
    border:none;
    border-radius:8px;
    padding:10px 20px;
    font-weight:600;
}

.stButton > button:hover {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
}

[data-testid="stSidebar"] {
    background:#020617;
}

.agent-card {
    background:#0f172a;
    padding:14px;
    border-radius:10px;
    border:1px solid #1e293b;
    margin-bottom:10px;
}

.log-box {
    background:#020617;
    padding:15px;
    border-radius:8px;
    border:1px solid #1e293b;
    height:350px;
    overflow-y:auto;
    font-family: monospace;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────

AGENT_ORDER = [
    "Business Analyst",
    "Design Agent",
    "Developer Agent",
    "Testing Agent"
]

STATUS_ICONS = {
    "pending": "⏳",
    "running": "🔄",
    "completed": "✅",
    "failed": "❌"
}

if "agent_statuses" not in st.session_state:
    st.session_state.agent_statuses = {a: "pending" for a in AGENT_ORDER}

if "comm_log" not in st.session_state:
    st.session_state.comm_log = []

if "results" not in st.session_state:
    st.session_state.results = None

if "completed" not in st.session_state:
    st.session_state.completed = False


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:

    st.title("🤖 Agent Status")
    st.markdown("---")

    for agent in AGENT_ORDER:

        status = st.session_state.agent_statuses.get(agent, "pending")
        icon = STATUS_ICONS.get(status, "⏳")

        st.markdown(
            f"""
            <div class="agent-card">
            {icon} <b>{agent}</b><br>
            Status: {status}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("AI-Powered Virtual Development Pod")


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.markdown("""
# 🚀 AI-Powered Virtual Development Pod

Simulate a **real AI software development team** that converts business ideas into working software using **collaborative AI agents**.
""")


# ─────────────────────────────────────────────
# Requirement Input
# ─────────────────────────────────────────────

requirement = st.text_area(
    "Project Requirement",
    placeholder="Example: Build a fraud detection platform",
    height=90
)

start = st.button("🚀 Start AI Development Pod")


# ─────────────────────────────────────────────
# Run Pipeline
# ─────────────────────────────────────────────

if start and requirement.strip():

    st.session_state.agent_statuses = {a: "pending" for a in AGENT_ORDER}
    st.session_state.comm_log = []
    st.session_state.results = None
    st.session_state.completed = False

    from agents.project_lead import ProjectLead

    lead = ProjectLead()

    def on_status(agent_name, status):

        st.session_state.agent_statuses[agent_name] = status

        ts = datetime.now().strftime("%H:%M:%S")

        st.session_state.comm_log.append(
            f"[{ts}] Project Lead → {agent_name}: {status}"
        )

    with st.status("Running AI Development Pod...", expanded=True):

        try:

            results = lead.run(
                requirement.strip(),
                on_status=on_status
            )

            st.session_state.results = results
            st.session_state.completed = True

            st.success("Pipeline completed successfully!")

        except Exception as e:

            st.error(f"Pipeline failed: {e}")

    st.rerun()


elif start and not requirement.strip():
    st.warning("Please enter a project requirement.")


# ─────────────────────────────────────────────
# Dashboard Layout
# ─────────────────────────────────────────────

st.markdown("---")

col1, col2 = st.columns([1,2])


# ─────────────────────────────────────────────
# Agent Status Panel
# ─────────────────────────────────────────────

with col1:

    st.subheader("⚙️ Agent Status Panel")

    for agent in AGENT_ORDER:

        status = st.session_state.agent_statuses.get(agent, "pending")
        icon = STATUS_ICONS.get(status, "⏳")

        st.markdown(
            f"""
            <div class="agent-card">
            {icon} <b>{agent}</b><br>
            Status: {status}
            </div>
            """,
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────
# Communication Log
# ─────────────────────────────────────────────

with col2:

    st.subheader("📡 Agent Communication Log")

    if st.session_state.comm_log:
        log_html = "<br>".join(st.session_state.comm_log[-20:])
    else:
        log_html = "Waiting for pod to start..."

    st.markdown(
        f"""
        <div class="log-box">
        {log_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# Artifact Viewer
# ─────────────────────────────────────────────

if st.session_state.completed and st.session_state.results:

    st.markdown("---")

    r = st.session_state.results

    tab_stories, tab_design, tab_code, tab_tests = st.tabs([
        "📋 User Stories",
        "🏗️ Design Document",
        "💻 Generated Code",
        "🧪 Test Cases"
    ])

    with tab_stories:
        st.markdown(r.get("user_stories", "*No output*"))

    with tab_design:
        st.markdown(r.get("design", "*No output*"))

    with tab_code:
        st.markdown(r.get("code", "*No output*"))

    with tab_tests:
        st.markdown(r.get("tests", "*No output*"))