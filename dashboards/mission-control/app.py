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

# ─── CONFIG ───────────────────────────────────────────────────────────────────

STATE_FILE = Path("/home/dusk/.openclaw/shared/state/agent-status.json")
REFRESH_INTERVAL = 30  # seconds
AWST_TZ = timezone(timedelta(hours=8))

# ─── FALLBACK STATE (for Streamlit Cloud) ──────────────────────────────────────

FALLBACK_STATE = {
    "last_updated": "2026-04-06T23:32:53+08:00",
    "agents": {
        "yuki": {"status": "idle", "last_run": "2026-04-06T23:00:00+08:00", "last_action": "Sent evening debrief to Dusk", "current_task": "Monitoring crew operations"},
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
    ]
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

# ─── AGENT CARDS ──────────────────────────────────────────────────────────────

if state and "agents" in state:
    agents = state["agents"]

    st.subheader("👥 Live Agent Status")

    # Row of agent cards
    card_cols = st.columns(len(agents))
    
    for idx, (agent_name, agent_data) in enumerate(agents.items()):
        with card_cols[idx]:
            status = agent_data.get("status", "unknown")
            emoji = status_emoji(status)
            bg = status_color(status)
            last_run = agent_data.get("last_run", "never")
            last_action = agent_data.get("last_action", "No action recorded")
            current_task = agent_data.get("current_task", "")
            next_run = agent_data.get("next_run", "")
            
            ago = get_time_ago(last_run)
            
            st.markdown(f"""
            <div style="background-color: {bg}; padding: 12px; border-radius: 10px; 
                        border: 1px solid #333; height: 180px; overflow: hidden;">
                <h4>{emoji} {agent_name.upper()}</h4>
                <p style="font-size: 11px; color: #aaa;">Last run: {ago}</p>
                <p style="font-size: 12px; margin-top: 5px;"><b>{last_action}</b></p>
                {f'<p style="font-size: 11px; color: #88f; margin-top: 5px;">🎯 {current_task}</p>' if current_task else ''}
                {f'<p style="font-size: 10px; color: #888; margin-top: 5px;">⏰ Next: {get_next_cron_ago(next_run)}</p>' if next_run else ''}
            </div>
            """, unsafe_allow_html=True)

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
