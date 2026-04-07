"""
DAWN LABS COMMAND CENTER — One Dashboard for Everything
Yuki's unified view of all operations

Run: streamlit run app.py
"""

import streamlit as st
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import os

st.set_page_config(page_title="Dawn Labs Command Center", page_icon="🚀", layout="wide")

# ─── CUSTOM THEME ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a12 0%, #0f0f1a 50%, #0a0a12 100%); }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stMetricValue { color: #00ff88 !important; font-weight: 700 !important; }
    .stMetricLabel { color: #8888aa !important; }
    hr { border-color: #2a2a3e !important; }
    .stCaption { color: #6666aa !important; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

AWST_TZ = timezone(timedelta(hours=8))

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def get_time_ago(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        now = datetime.now(AWST_TZ)
        diff = now - dt.astimezone(AWST_TZ)
        hours = diff.total_seconds() / 3600
        if hours < 1: return f"{int(hours*60)}m ago"
        if hours < 24: return f"{int(hours)}h ago"
        return f"{int(hours/24)}d ago"
    except:
        return "unknown"

def read_file(path):
    try:
        with open(path) as f:
            return f.read()[:2000]  # Limit for display
    except:
        return None

def get_latest_file(directory, pattern="*"):
    try:
        files = list(Path(directory).glob(pattern))
        if files:
            latest = max(files, key=lambda p: p.stat().st_mtime)
            return latest
    except:
        pass
    return None

# ─── HEADER ──────────────────────────────────────────────────────────────────

st.title("🚀 DAWN LABS COMMAND CENTER")
st.caption(f"Last updated: {datetime.now(AWST_TZ).strftime('%Y-%m-%d %H:%M AWST')}")
st.divider()

# ─── QUICK STATS ROW ──────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

with col1:
    harold_file = get_latest_file("/home/dusk/.openclaw/shared/research/happy-harold/daily", "*.md")
    if harold_file:
        st.metric("📡 Harold Research", "Updated", get_time_ago(datetime.fromtimestamp(harold_file.stat().st_mtime).isoformat()))
    else:
        st.metric("📡 Harold Research", "—", "No file")

with col2:
    maya_file = get_latest_file("/home/dusk/.openclaw/shared/research/maya", "*.md")
    if maya_file:
        st.metric("✍️ Maya Content", "Updated", get_time_ago(datetime.fromtimestamp(maya_file.stat().st_mtime).isoformat()))
    else:
        st.metric("✍️ Maya Content", "—", "No file")

with col3:
    emmy_file = get_latest_file("/home/dusk/.openclaw/shared/research/emmy", "*.md")
    if emmy_file:
        st.metric("🔨 Emmy Builds", "Updated", get_time_ago(datetime.fromtimestamp(emmy_file.stat().st_mtime).isoformat()))
    else:
        st.metric("🔨 Emmy Builds", "—", "No file")

with col4:
    karma_file = get_latest_file("/home/dusk/.openclaw/workspace/yuki/emvy/prospects", "*.md")
    if karma_file:
        st.metric("💰 EMVY Leads", "Updated", get_time_ago(datetime.fromtimestamp(karma_file.stat().st_mtime).isoformat()))
    else:
        st.metric("💰 EMVY Leads", "—", "No file")

st.divider()

# ─── RESEARCH SECTION ─────────────────────────────────────────────────────────

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📡 Latest Research (Harold)")
    
    research_file = get_latest_file("/home/dusk/.openclaw/shared/research/happy-harold/daily", "*.md")
    if research_file:
        with open(research_file) as f:
            content = f.read()[:1500]
        st.markdown(f"**File:** `{research_file.name}`")
        st.markdown(content)
    else:
        st.info("No research files found")

with col_right:
    st.subheader("✍️ Latest Content (Maya)")
    
    maya_output = get_latest_file("/home/dusk/.openclaw/shared/research/maya", "*.md")
    if maya_output:
        with open(maya_output) as f:
            content = f.read()[:1500]
        st.markdown(f"**File:** `{maya_output.name}`")
        st.markdown(content)
    else:
        st.info("No content files found")

st.divider()

# ─── BUILDS SECTION ──────────────────────────────────────────────────────────

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔨 Latest Build (Emmy)")
    
    emmy_build = get_latest_file("/home/dusk/.openclaw/shared/research/emmy", "*.md")
    if emmy_build:
        with open(emmy_build) as f:
            content = f.read()[:1500]
        st.markdown(f"**File:** `{emmy_build.name}`")
        st.markdown(content)
    else:
        st.info("No build files found")

with col_right:
    st.subheader("💰 Latest Leads (Karma)")
    
    karma_leads = get_latest_file("/home/dusk/.openclaw/workspace/yuki/emvy/prospects", "*.md")
    if karma_leads:
        with open(karma_leads) as f:
            content = f.read()[:1500]
        st.markdown(f"**File:** `{karma_leads.name}`")
        st.markdown(content)
    else:
        st.info("No lead files found")

st.divider()

# ─── SYSTEM STATUS ────────────────────────────────────────────────────────────

st.subheader("🔧 System Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.markdown("**Agents**")
    agents = ["yuki", "harold", "maya", "emmy", "karma", "connor", "chad", "hermes"]
    for agent in agents:
        st.write(f"• {agent.upper()} — 🟢 ok")

with status_col2:
    st.markdown("**Daily Crew**")
    crew = [
        ("Harold", "8 AM", "Research"),
        ("Maya", "9 AM", "Content"),
        ("Emmy", "10 AM", "Build"),
    ]
    for name, time, role in crew:
        st.write(f"• {name} — {time} AWST — {role}")

with status_col3:
    st.markdown("**Brand Architecture**")
    brands = [
        "Dawn Labs (Parent)",
        "EMVY AI (Audits)",
        "Shut Up and Build (YouTube)",
        "AI My Guy (Newsletter)",
    ]
    for brand in brands:
        st.write(f"• {brand}")

st.divider()

# ─── QUICK ACTIONS ────────────────────────────────────────────────────────────

st.subheader("⚡ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📡 Run Harold Research Now"):
        st.info("Spawning Harold... (would trigger subagent)")

with action_col2:
    if st.button("✍️ Run Maya Content Now"):
        st.info("Spawning Maya... (would trigger subagent)")

with action_col3:
    if st.button("🔨 Run Emmy Build Now"):
        st.info("Spawning Emmy... (would trigger subagent)")

st.divider()

# ─── FOOTER ──────────────────────────────────────────────────────────────────

st.caption("Dawn Labs Command Center — Built by Yuki | Shut Up and Build 🚀")
