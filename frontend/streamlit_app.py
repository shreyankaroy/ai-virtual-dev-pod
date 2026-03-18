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
    height:500px;
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

col2 = st.container()


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


# ─────────────────────────────────────────────
# 🕒 Replay / Time Travel Mode
# ─────────────────────────────────────────────

import time as _time
from replay.replay_engine import ReplayEngine

st.markdown("---")
st.subheader("🕒 Replay Mode")
st.caption("Interactive step-by-step execution replay with playback controls.")

# --- Session state defaults ---
for _key, _default in [
    ("replay_step_index", 0),
    ("replay_is_playing", False),
    ("replay_run_data", None),
    ("replay_selected_file", None),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default

replay_engine = ReplayEngine()
available_runs = replay_engine.list_runs()

if available_runs:

    selected_run = st.selectbox(
        "Select Execution Run",
        available_runs,
        format_func=lambda f: f.replace(".json", "").replace("_", " ").title(),
        key="replay_run_selector",
    )

    # --- Load / Reset when a new run is selected or "Replay" is clicked ---
    def _start_replay():
        try:
            data = replay_engine.load_run(selected_run)
            steps = data.get("steps", [])
            if not steps:
                st.session_state.replay_run_data = None
                return
            st.session_state.replay_run_data = data
            st.session_state.replay_selected_file = selected_run
            st.session_state.replay_step_index = 0
            st.session_state.replay_is_playing = False
        except (ValueError, KeyError, FileNotFoundError):
            st.session_state.replay_run_data = None

    st.button("🔄 Load & Replay", on_click=_start_replay)

    # Reset if user picks a different run file
    if st.session_state.replay_selected_file != selected_run:
        st.session_state.replay_run_data = None

    # --- Playback UI ---
    run_data = st.session_state.replay_run_data

    if run_data is not None:
        steps = run_data.get("steps", [])
        total = len(steps)
        idx = st.session_state.replay_step_index

        # Clamp index
        idx = max(0, min(idx, total - 1))
        st.session_state.replay_step_index = idx

        # Run metadata
        st.markdown(
            f"**Run:** {run_data.get('run_id', 'N/A')} &nbsp;|&nbsp; "
            f"**Started:** {run_data.get('started_at', 'N/A')} &nbsp;|&nbsp; "
            f"**Completed:** {run_data.get('completed_at', 'N/A')}"
        )

        # Progress bar
        st.progress((idx + 1) / total, text=f"Step {idx + 1} of {total}")

        # --- Control buttons ---
        ctrl_cols = st.columns([1, 1, 1, 1, 2])

        with ctrl_cols[0]:
            if st.button("⏮ Prev", disabled=(idx == 0)):
                st.session_state.replay_step_index = max(idx - 1, 0)
                st.session_state.replay_is_playing = False
                st.rerun()

        with ctrl_cols[1]:
            if st.button("⏭ Next", disabled=(idx >= total - 1)):
                st.session_state.replay_step_index = min(idx + 1, total - 1)
                st.session_state.replay_is_playing = False
                st.rerun()

        with ctrl_cols[2]:
            if st.button("▶️ Play", disabled=st.session_state.replay_is_playing):
                st.session_state.replay_is_playing = True
                st.rerun()

        with ctrl_cols[3]:
            if st.button("⏸ Pause", disabled=not st.session_state.replay_is_playing):
                st.session_state.replay_is_playing = False
                st.rerun()

        # --- Current step display ---
        step = steps[idx]
        icon = STATUS_ICONS.get(step.get("status", ""), "⏳")
        status_color = "#22c55e" if step.get("status") == "completed" else (
            "#f59e0b" if step.get("status") == "running" else "#ef4444"
        )

        st.markdown(
            f"""
            <div style="background:#0f172a; padding:18px; border-radius:12px;
                        border:2px solid {status_color}; margin:10px 0;">
                <div style="font-size:13px; color:#94a3b8; margin-bottom:6px;">
                    🕐 {step.get('timestamp', '')}
                </div>
                <div style="font-size:20px; font-weight:700; color:#e2e8f0;">
                    {icon} {step.get('agent_name', 'Unknown')}
                    <span style="font-size:14px; color:{status_color};
                                 margin-left:10px;">{step.get('status', '').upper()}</span>
                </div>
                {"<div style='margin-top:10px; color:#cbd5e1;'><b>Input:</b> " + step['input_data'] + "</div>" if step.get('input_data') else ""}
                {"<div style='margin-top:6px; color:#cbd5e1;'><b>Output:</b> " + (step['output_data'][:300] + "…" if len(step.get('output_data','')) > 300 else step.get('output_data','')) + "</div>" if step.get('output_data') else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Timeline overview (mini) ---
        timeline_html = ""
        for i, s in enumerate(steps):
            is_current = (i == idx)
            s_icon = STATUS_ICONS.get(s.get("status", ""), "⏳")
            bg = "#1e3a5f" if is_current else "#0f172a"
            border = status_color if is_current else "#1e293b"
            timeline_html += (
                f'<div style="display:inline-block; padding:6px 12px; margin:3px;'
                f' border-radius:8px; border:1px solid {border}; background:{bg};'
                f' font-size:12px; color:#e2e8f0;">'
                f'{s_icon} {s.get("agent_name", "?")}</div>'
            )

        st.markdown(
            f'<div style="margin-top:12px;">{timeline_html}</div>',
            unsafe_allow_html=True,
        )

        # --- Auto-play loop ---
        if st.session_state.replay_is_playing and idx < total - 1:
            _time.sleep(1.5)
            st.session_state.replay_step_index = idx + 1
            st.rerun()
        elif st.session_state.replay_is_playing and idx >= total - 1:
            st.session_state.replay_is_playing = False

    elif st.session_state.replay_selected_file is not None:
        st.warning("Selected run log is empty or corrupted. Choose another run.")

else:
    st.info("No execution logs found yet. Run the pipeline to generate logs.")