"""
MISSION CONTROL DASHBOARD — LIVE
Yuki's Command Center — Real-time Agent Monitoring

Run: streamlit run app.py
Auto-refresh: every 30 seconds
State file: /home/dusk/.openclaw/shared/state/agent-status.json
"""

import streamlit as st
import json
from datetime import datetime, timezone, timedelta
import os
from pathlib import Path

st.set_page_config(page_title="🚀 Mission Control", page_icon="🚀", layout="wide")

# ─── CUSTOM THEME CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a12 0%, #0f0f1a 50%, #0a0a12 100%);
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cards and containers */
    .stCard, div[data-testid="stVerticalBlock"] > div {
        background-color: #12121a !important;
        border-radius: 12px;
    }
    
    /* Success/Info boxes */
    .stAlert {
        background-color: #1a1a2e !important;
        border: 1px solid #2a2a3e !important;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8888aa !important;
    }
    
    /* Dividers */
    hr {
        border-color: #2a2a3e !important;
        margin: 1rem 0 !important;
    }
    
    /* Sidebar / expanders */
    .streamlit-expanderHeader {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
        color: #0a0a12 !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px #00ff8866 !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff88 0%, #00cc6a 100%) !important;
    }
    
    /* Text colors */
    .stCaption {
        color: #6666aa !important;
    }
    
    /* Links */
    a {
        color: #00ff88 !important;
        text-decoration: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a12;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a2a3e;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a4e;
    }
    
    /* Glow effects on cards */
    .glow-card {
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    /* Status colors */
    .status-ok { color: #00ff88 !important; }
    .status-idle { color: #888 !important; }
    .status-running { color: #4a9eff !important; }
    .status-error { color: #ff4444 !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONFIG ───────────────────────────────────────────────────────────────────

STATE_FILE = Path("/home/dusk/.openclaw/shared/state/agent-status.json")
REFRESH_INTERVAL = 30  # seconds
AWST_TZ = timezone(timedelta(hours=8))

# ─── FALLBACK STATE (for Streamlit Cloud) ──────────────────────────────────────

FALLBACK_STATE = {
    "last_updated": "2026-04-06T23:32:53+08:00",
    "agents": {
        "yuki": {"status": "idle", "last_run": "2026-04-06T23:00:00+08:00", "last_action": "Sent evening debrief to Dusk", "current_task": "Monitoring crew operations"},
        "hermes": {"status": "ok", "last_run": "2026-04-06T23:00:00+08:00", "last_action": "Strategic advisory — reviewing operations", "current_task": "Supervising with Yuki"},
        "harold": {"status": "ok", "last_run": "2026-04-06T08:00:00+08:00", "last_action": "18 searches complete — SMB industry deep dive", "next_run": "2026-04-07T08:00:00+08:00"},
        "maya": {"status": "ok", "last_run": "2026-04-06T09:00:00+08:00", "last_action": "3 draft posts delivered to Dusk", "next_run": "2026-04-07T09:00:00+08:00"},
        "emmy": {"status": "ok", "last_run": "2026-04-06T23:32:00+08:00", "last_action": "Mission Control live dashboard deployed", "next_run": "2026-04-07T10:00:00+08:00", "current_task": "Building next SaaS"},
        "karma": {"status": "ok", "last_run": "2026-04-06T10:30:00+08:00", "last_action": "EMVY outreach — 18 emails sent today", "next_run": "2026-04-07T10:30:00+08:00"},
        "connor": {"status": "idle", "last_run": "2026-04-06T11:00:00+08:00", "last_action": "2 audits queued — awaiting client responses", "next_run": "2026-04-07T11:00:00+08:00"},
        "chad": {"status": "idle", "last_run": "2026-04-06T12:00:00+08:00", "last_action": "EMVY build — Calendly integration wired", "next_run": "2026-04-07T12:00:00+08:00"}
    },
    "emvy": {"leads_total": 57, "leads_new_today": 3, "emails_sent_today": 18, "emails_pending": 7, "bookings": 0, "audits_in_progress": 2},
    "upcoming_crons": [
        {"name": "Yuki Morning Briefing", "next_run": "2026-04-07T09:00:00+08:00", "agent": "yuki"},
        {"name": "Happy Harold Daily Research", "next_run": "2026-04-07T08:00:00+08:00", "agent": "harold"},
        {"name": "Maya Content Scan", "next_run": "2026-04-07T09:00:00+08:00", "agent": "maya"},
        {"name": "Emmy Build Intel", "next_run": "2026-04-07T10:00:00+08:00", "agent": "emmy"},
        {"name": "Karma EMVY Outreach", "next_run": "2026-04-07T10:30:00+08:00", "agent": "karma"},
        {"name": "Connor Audit Check", "next_run": "2026-04-07T11:00:00+08:00", "agent": "connor"},
        {"name": "Chad Build Sync", "next_run": "2026-04-07T12:00:00+08:00", "agent": "chad"}
    ],
    "workflows": {
        "emvy": {
            "status": "active", "name": "EMVY AI",
            "description": "Client pipeline + revenue",
            "steps": ["Lead Gen", "Email Outreach", "Book Call", "Audit", "Build", "Retainer"],
            "current_step": 2,
            "stats": {"leads": 57, "booked": 0, "audits": 2, "clients": 0},
            "next_action": "Follow up with warm leads"
        },
        "youtube": {
            "status": "building", "name": "YouTube Channel",
            "description": "Shut Up and Build — AI Agent content",
            "steps": ["Channel Setup", "Script", "Avatar Video", "Publish", "Monetize"],
            "current_step": 2,
            "stats": {"videos": 0, "subscribers": 0, "views": 0},
            "next_action": "Create YouTube channel"
        },
        "personal_brand": {
            "status": "active", "name": "Personal Brand",
            "description": "Dusk's X presence + authority",
            "steps": ["Research", "Content", "Engagement", "Growth"],
            "current_step": 2,
            "stats": {"followers": 0, "posts_week": 0, "engagement": "—"},
            "next_action": "Post 3x today on X"
        },
        "newsletter": {
            "status": "planned", "name": "Newsletter",
            "description": "Weekly newsletter funnel to EMVY",
            "steps": ["Substack Setup", "Lead Magnet", "First Issue", "Grow List"],
            "current_step": 0,
            "stats": {"subscribers": 0, "open_rate": "—", "issues_sent": 0},
            "next_action": "Create Substack account"
        }
    }
}

# ─── AUTH GATE ─────────────────────────────────────────────────────────────────

# Check for bypass mode (Streamlit Cloud secrets)
try:
    bypass_auth = st.secrets.get("BYPASS_PIN", False)
except Exception:
    bypass_auth = False

if not bypass_auth:
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔒 Mission Control — Login")
        password = st.text_input("Enter PIN", type="password")
        if password:
            if password == st.secrets["PIN"]:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect PIN")
        st.stop()
else:
    st.session_state["authenticated"] = True

# Mode banner
if STATE_FILE.exists():
    st.success("🟢 LIVE — Reading from local agent-status.json")
else:
    st.info("📡 CLOUD MODE — Showing last known state (static). Local = live data.")

# ─── AUTO REFRESH ─────────────────────────────────────────────────────────────

try:
    st_autorefresh = st.autorefresh(interval=REFRESH_INTERVAL * 1000, key="live_refresh")
except Exception:
    # Fallback for older Streamlit versions — meta refresh
    st.markdown(
        f"<meta http-equiv=\"refresh\" content=\"{REFRESH_INTERVAL}\">",
        unsafe_allow_html=True
    )
    st.caption(f"⏱ Auto-refresh every {REFRESH_INTERVAL}s (legacy mode)")

# ─── STATE LOADER ─────────────────────────────────────────────────────────────

def load_state():
    """Load agent status from shared state file, fallback to embedded data."""
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        else:
            # Return fallback state for cloud deployments
            return FALLBACK_STATE
    except Exception:
        return FALLBACK_STATE

def get_time_ago(dt_str):
    """Return human-readable time ago string."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        now = datetime.now(AWST_TZ)
        diff = now - dt
        total_seconds = diff.total_seconds()
        if total_seconds < 60:
            return f"{int(total_seconds)}s ago"
        elif total_seconds < 3600:
            return f"{int(total_seconds / 60)}m ago"
        elif total_seconds < 86400:
            return f"{int(total_seconds / 3600)}h ago"
        else:
            return f"{int(total_seconds / 86400)}d ago"
    except:
        return "unknown"

def get_next_cron_ago(next_run_str):
    """Return time until next cron run."""
    try:
        next_run = datetime.fromisoformat(next_run_str.replace("Z", "+00:00"))
        now = datetime.now(AWST_TZ)
        diff = next_run - now
        total_seconds = diff.total_seconds()
        if total_seconds < 0:
            return "OVERDUE"
        elif total_seconds < 3600:
            return f"in {int(total_seconds / 60)}m"
        elif total_seconds < 86400:
            return f"in {int(total_seconds / 3600)}h"
        else:
            return f"in {int(total_seconds / 86400)}d"
    except:
        return "unknown"

def status_emoji(status):
    """Map status to emoji."""
    mapping = {
        "ok": "🟢",
        "idle": "🟡",
        "running": "🔵",
        "error": "🔴",
    }
    return mapping.get(status.lower(), "⚪")

def status_color(status):
    """Map status to hex color."""
    mapping = {
        "ok": "#1a3a1a",
        "idle": "#2a2a1a",
        "running": "#0a1a3a",
        "error": "#3a1a1a",
    }
    return mapping.get(status.lower(), "#1a1a2e")

# ─── LOAD STATE ────────────────────────────────────────────────────────────────

state = load_state()
now_str = datetime.now(AWST_TZ).strftime("%Y-%m-%d %H:%M:%S AWST")

# ─── HEADER ───────────────────────────────────────────────────────────────────

st.title("🚀 MISSION CONTROL — LIVE")
col1, col2 = st.columns([3, 1])
with col1:
    st.caption(f"🕐 {now_str} | Auto-refresh every {REFRESH_INTERVAL}s")
with col2:
    if state:
        last_updated = state.get("last_updated", "unknown")
        st.caption(f"📡 State updated: {get_time_ago(last_updated)}")

st.divider()

# ─── ORG CHART ───────────────────────────────────────────────────────────────

st.subheader("🧭 Organization Chart")

# YUKI + HERMES — co-supervisors at top
supervisor_cols = st.columns([1, 1])

with supervisor_cols[0]:
    st.markdown("""
    <div style="text-align: center; padding: 15px;">
        <img src="https://raw.githubusercontent.com/duskmetamask-bit/workspace-yuki/main/studios/ai-agent-studio/assets/yuki-pfp.jpg" 
             width="80" style="border-radius: 50%; border: 3px solid #00ff88; box-shadow: 0 0 20px #00ff8844;">
        <h3 style="color: #00ff88; margin: 8px 0 3px 0;">YUKI</h3>
        <p style="color: #888; font-size: 10px; margin: 0;">CEO — COORDINATOR</p>
        <p style="color: #aaa; font-size: 10px; margin-top: 5px;">🟢 ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

with supervisor_cols[1]:
    st.markdown("""
    <div style="text-align: center; padding: 15px;">
        <img src="https://raw.githubusercontent.com/duskmetamask-bit/workspace-yuki/main/studios/ai-agent-studio/assets/hermes-pfp.jpg" 
             width="80" style="border-radius: 50%; border: 3px solid #4a9eff; box-shadow: 0 0 20px #4a9eff44;">
        <h3 style="color: #4a9eff; margin: 8px 0 3px 0;">HERMES</h3>
        <p style="color: #888; font-size: 10px; margin: 0;">STRATEGIC ADVISOR</p>
        <p style="color: #aaa; font-size: 10px; margin-top: 5px;">🟢 SUPERVISOR</p>
    </div>
    """, unsafe_allow_html=True)

# Connector line
st.markdown("<div style="text-align: center;"><span style="color: #333;">│</span></div>", unsafe_allow_html=True)
st.markdown("<div style="text-align: center;"><span style="color: #00ff88;">▼</span></div>", unsafe_allow_html=True)

# Personal Brand track label
st.markdown("<p style="text-align: center; color: #666; font-size: 11px; margin: 5px 0;">PERSONAL BRAND TRACK</p>", unsafe_allow_html=True)

# Row 2: Harold, Maya, Emmy (Personal Brand)
brand_agents = ["harold", "maya", "emmy"]
brand_col = st.columns(3)

for idx, agent_name in enumerate(brand_agents):
    if state and "agents" in state and agent_name in state["agents"]:
        agent_data = state["agents"][agent_name]
        with brand_col[idx]:
            status = agent_data.get("status", "unknown")
            emoji = status_emoji(status)
            bg = status_color(status)
            last_action = agent_data.get("last_action", "No action recorded")
            
            # Role labels
            roles = {"harold": "RESEARCH", "maya": "CONTENT", "emmy": "BUILDER"}
            role = roles.get(agent_name, "")
            
            st.markdown(f"""
            <div style="background-color: {bg}; padding: 15px; border-radius: 10px; 
                        border: 1px solid #333; text-align: center; height: 150px;">
                <h4 style="color: #fff; margin: 0;">{emoji} {agent_name.upper()}</h4>
                <p style="color: #00ff88; font-size: 10px; margin: 3px 0;">{role}</p>
                <p style="color: #888; font-size: 11px; margin-top: 10px;">{last_action[:50]}...</p>
            </div>
            """, unsafe_allow_html=True)

# Connector
st.markdown("<div style="text-align: center; margin: 10px 0;"><span style="color: #00ff88;">▼</span></div>", unsafe_allow_html=True)

# EMVY track label  
st.markdown("<p style="text-align: center; color: #666; font-size: 11px; margin: 5px 0;">EMVY BUSINESS TRACK</p>", unsafe_allow_html=True)

# Row 3: Karma, Connor, Chad (EMVY)
emvy_agents = ["karma", "connor", "chad"]
emvy_col = st.columns(3)

for idx, agent_name in enumerate(emvy_agents):
    if state and "agents" in state and agent_name in state["agents"]:
        agent_data = state["agents"][agent_name]
        with emvy_col[idx]:
            status = agent_data.get("status", "unknown")
            emoji = status_emoji(status)
            bg = status_color(status)
            last_action = agent_data.get("last_action", "No action recorded")
            
            roles = {"karma": "LEAD GEN", "connor": "AUDIT", "chad": "BUILD"}
            role = roles.get(agent_name, "")
            
            st.markdown(f"""
            <div style="background-color: {bg}; padding: 15px; border-radius: 10px; 
                        border: 1px solid #333; text-align: center; height: 150px;">
                <h4 style="color: #fff; margin: 0;">{emoji} {agent_name.upper()}</h4>
                <p style="color: #f5a623; font-size: 10px; margin: 3px 0;">{role}</p>
                <p style="color: #888; font-size: 11px; margin-top: 10px;">{last_action[:50]}...</p>
            </div>
            """, unsafe_allow_html=True)

st.divider()

    st.divider()

    # ─── RECENT ACTIONS FEED ──────────────────────────────────────────────────

    st.subheader("📋 Recent Actions Feed")

    feed_items = []
    for agent_name, agent_data in agents.items():
        last_action = agent_data.get("last_action", "")
        last_run = agent_data.get("last_run", "")
        status = agent_data.get("status", "unknown")
        if last_action and last_action != "No action recorded":
            feed_items.append({
                "agent": agent_name,
                "action": last_action,
                "time": get_time_ago(last_run),
                "status": status
            })

    # Sort by recency (most recent first)
    feed_items.sort(key=lambda x: x["time"], reverse=False)

    for item in feed_items:
        emoji = status_emoji(item["status"])
        st.markdown(f"""
        <div style="padding: 6px 10px; margin: 4px 0; background-color: #1a1a2e; 
                    border-radius: 6px; border-left: 3px solid #333;">
            <span style="font-weight: bold; color: #7af;">{emoji} {item['agent']}</span>
            <span style="color: #888; font-size: 11px; margin-left: 8px;">{item['time']}</span><br>
            <span style="font-size: 12px;">{item['action']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ─── EMVY PIPELINE STATUS ───────────────────────────────────────────────

    st.subheader("📊 EMVY Pipeline Status")

    if "emvy" in state:
        emvy = state["emvy"]
        e1, e2, e3, e4, e5 = st.columns(5)
        
        with e1:
            st.metric("Total Leads", emvy.get("leads_total", 0))
        with e2:
            st.metric("New Today", emvy.get("leads_new_today", 0))
        with e3:
            st.metric("Emails Sent Today", emvy.get("emails_sent_today", 0))
        with e4:
            st.metric("Pending", emvy.get("emails_pending", 0))
        with e5:
            st.metric("Bookings", emvy.get("bookings", 0))

        # Audits in progress
        audits = emvy.get("audits_in_progress", 0)
        if audits > 0:
            st.info(f"🔍 {audits} audit(s) in progress — awaiting client responses")

    st.divider()

    # ─── WORKFLOWS / TRACKS ─────────────────────────────────────────────────

    st.subheader("🚀 Active Workflows")

    if "workflows" in state:
        workflows = state["workflows"]
        
        wf_cols = st.columns(len(workflows))
        
        for idx, (wf_key, wf) in enumerate(workflows.items()):
            with wf_cols[idx]:
                status = wf.get("status", "unknown")
                name = wf.get("name", wf_key)
                desc = wf.get("description", "")
                stats = wf.get("stats", {})
                next_action = wf.get("next_action", "")
                
                # Status color
                if status == "active":
                    status_emoji = "🟢"
                    status_color = "#00cc6a"
                elif status == "building":
                    status_emoji = "🟡"
                    status_color = "#f5a623"
                elif status == "planned":
                    status_emoji = "🔵"
                    status_color = "#4a9eff"
                else:
                    status_emoji = "⚪"
                    status_color = "#666"
                
                # Build stats display
                stats_html = ""
                for k, v in stats.items():
                    stats_html += f'<p style="font-size: 12px; margin: 3px 0;">{k}: <b>{v}</b></p>'
                
                # Progress through steps
                steps = wf.get("steps", [])
                current_step = wf.get("current_step", 0)
                steps_html = ""
                for i, step in enumerate(steps):
                    if i < current_step:
                        steps_html += f'<span style="color: #00ff88;">✓</span> '
                    elif i == current_step:
                        steps_html += f'<span style="color: #f5a623;">●</span> '
                    else:
                        steps_html += f'<span style="color: #444;">○</span> '
                steps_html += f'<span style="font-size: 10px; color: #666;"> step {current_step+1}/{len(steps)}</span>'
                
                st.markdown(f"""
                <div style="background-color: #1a1a2e; padding: 15px; border-radius: 10px; 
                            border: 1px solid #333; height: 220px; overflow: hidden;">
                    <h4>{status_emoji} {name}</h4>
                    <p style="font-size: 10px; color: #888;">{desc}</p>
                    <div style="margin: 8px 0;">{steps_html}</div>
                    <div style="margin: 8px 0;">{stats_html}</div>
                    <p style="font-size: 11px; color: #f5a623; margin-top: 5px;">▶ {next_action}</p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # ─── UPCOMING CRONS ─────────────────────────────────────────────────────

    st.subheader("⏰ Today's Schedule")

    if "upcoming_crons" in state and state["upcoming_crons"]:
        # Sort by next_run time
        crons = sorted(state["upcoming_crons"], 
                       key=lambda x: x.get("next_run", "9999"))
        
        for cron in crons:
            name = cron.get("name", "Unknown")
            next_run = cron.get("next_run", "")
            agent = cron.get("agent", "")
            when = get_next_cron_ago(next_run) if next_run else "unknown"
            
            st.markdown(f"""
            <div style="padding: 6px 10px; margin: 4px 0; background-color: #1a1a2e; 
                        border-radius: 6px;">
                <span style="font-weight: bold;">🕐 {name}</span>
                <span style="color: #888; font-size: 11px;"> — {agent}</span>
                <span style="float: right; color: #aaa;">{when}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No upcoming crons scheduled")



st.divider()

# ─── LEGACY SECTIONS (static reference) ───────────────────────────────────────

with st.expander("📌 The 4 Pillars (static reference)"):
    pillars = [
        {
            "num": "1st", "name": "EMVY AI AUDIT", "goal": "Get clients, close deals",
            "done_when": "34 cold emails sent + 3+ replies + 1+ booked call",
            "status": "🔴 BLOCKED", "active": False,
            "items": [
                ("Cold email outreach → 34 leads", "🔴", "Gmail app password needed"),
                ("Calendly → Discovery Form auto-email", "🟢", "Built — waiting on Gmail"),
            ]
        },
        {
            "num": "2nd", "name": "RESEARCH + OPPORTUNITIES", "goal": "Scan market, find angles",
            "done_when": "5+ actionable leads OR content ideas saved",
            "status": "🟡 AVAILABLE", "active": False,
            "items": [
                ("Money opportunities", "🟢", "Felix running"),
                ("AI news + releases", "🟢", "Happy Harold running"),
                ("Content briefs + drafts", "🟡", "Maya working"),
                ("Daily synthesis", "🟢", "Chen running"),
            ]
        },
        {
            "num": "3rd", "name": "BUILD FROM RESEARCH", "goal": "Content app, pages, copy, funnels",
            "done_when": "RepurposeKit deployed OR landing page updated",
            "status": "🟢 ACTIVE", "active": True,
            "items": [
                ("RepurposeKit MVP", "🟡", "Deploy pending — needs Render connect"),
                ("Landing page", "🟢", "Live at emvy-site.vercel.app"),
                ("Cold email scripts", "🟢", "Done"),
                ("Follow-up E2 script", "🟢", "Done"),
                ("Lead CRM", "🟢", "Done"),
                ("Outreach talk track", "🟢", "Done"),
                ("Email verifier", "🟢", "Done"),
                ("Case study template", "🟢", "Done"),
                ("Gmail Calendly watcher", "🟢", "Done"),
            ]
        },
        {
            "num": "4th", "name": "SHIP SaaS PRODUCTS", "goal": "Deploy micro-SaaS, test",
            "done_when": "1 app live + first sign-up OR test results",
            "status": "🟡 NEXT UP", "active": False,
            "items": [
                ("RepurposeKit", "🟡", "Deploy when P3 done"),
                ("AI Readiness Tool", "🟡", "Deploy when P3 done"),
                ("MeetingMind, CV Tailor", "🟢", "Ready"),
                ("Teacher Marker", "🟡", "NEW — Emmy building"),
            ]
        },
    ]

    for p in pillars:
        color = "background-color: #1a3a1a" if p["active"] else "background-color: #1a1a2e"
        
        with st.container():
            if p["active"]:
                st.markdown(f"""
                <div style="{color}; padding: 15px; border-radius: 10px; border: 2px solid #00ff00; margin-bottom: 10px;">
                <h3>{p['num']} — {p['name']} {p['status']}</h3>
                <p><b>Goal:</b> {p['goal']}</p>
                <p><b>Done when:</b> {p['done_when']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="{color}; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px;">
                <h3>{p['num']} — {p['name']} {p['status']}</h3>
                <p><b>Goal:</b> {p['goal']}</p>
                <p><b>Done when:</b> {p['done_when']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            items_data = [(i[0], i[1], i[2]) for i in p["items"]]
            if items_data:
                st.table(items_data)
            st.markdown("---")

with st.expander("🔔 Flags for Dusk"):
    flags_data = [
        ("Gmail app password", "Unblocks Pillar 1 → cold emails fire"),
        ("Connect RepurposeKit on Render", "Unblocks Pillar 3 → deploys"),
    ]
    st.table(flags_data)

with st.expander("✅ Done This Week"):
    wins = [
        "Workspace backed up to GitHub",
        "Cold email scripts built (ready to fire)",
        "34 verified leads in CRM",
        "RepurposeKit code ready",
        "VisualForge MVP built",
        "Landing page live",
        "Base Scout deployed",
        "Daily ops crons cleaned up",
        "Teacher Marker build track started",
    ]
    for w in wins:
        st.markdown(f"- {w}")

with st.expander("🔗 Quick Links"):
    links = [
        ("EMVY Landing Page", "https://emvy-site.vercel.app"),
        ("EMVY Discovery Form", "https://docs.google.com/forms/d/1WMdAFb9zbdJBvKQEO1xvgXWAalJAymB5NfRvCsGpmJY/viewform"),
        ("EMVY Calendly", "https://calendly.com/emvyai"),
        ("Lead CRM", "/home/dusk/.openclaw/shared/karma/pipeline/lead-crm.md"),
        ("Research", "/home/dusk/.openclaw/shared/research/"),
        ("Emmy Builds", "/home/dusk/.openclaw/workspace/emmy/memory/emmy-output/"),
    ]
    for name, url in links:
        st.markdown(f"- [{name}]({url})")
