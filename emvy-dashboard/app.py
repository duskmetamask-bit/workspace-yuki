"""
EMVY AUDIT DASHBOARD — Complete Business Command Center
Yuki's EMVY AI Audit Business Dashboard

Run: streamlit run app.py
"""

import streamlit as st
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

st.set_page_config(page_title="EMVY Audit Dashboard", page_icon="💰", layout="wide")

# ─── CONFIG ───────────────────────────────────────────────────────────────────

AWST_TZ = timezone(timedelta(hours=8))

# ─── FALLBACK DATA ───────────────────────────────────────────────────────────

FALLBACK_DATA = {
    "leads": {
        "total": 57,
        "new_today": 3,
        "qualified": 18,
        "unqualified": 39,
        "by_industry": {
            "Wellness": 12,
            "E-commerce": 10,
            "SaaS/Tech": 8,
            "Fashion": 7,
            "Food & Beverage": 6,
            "Healthcare": 5,
            "Legal": 3,
            "Finance": 3,
            "Other": 3
        }
    },
    "emails": {
        "sent": 57,
        "delivered": 57,
        "opened": 12,
        "replied": 3,
        "failed": 0,
        "pending": 7,
        "open_rate": "21%",
        "reply_rate": "5%"
    },
    "calendly": {
        "booked": 0,
        "completed": 0,
        "upcoming": 0,
        "no_show": 0
    },
    "audits": {
        "in_progress": 2,
        "completed": 0,
        "pending_payment": 0,
        "upgraded_to_build": 0
    },
    "revenue": {
        "audits_total": 0,
        "builds_total": 0,
        "retainers_total": 0,
        "monthly_recurring": 0,
        "target_monthly": 1500,
        "target_quarterly": 15000
    },
    "funnel": {
        "leads": 57,
        "contacted": 50,
        "interested": 5,
        "booked": 0,
        "audit_started": 0,
        "audit_completed": 0,
        "build_started": 0,
        "retainer": 0
    },
    "kpis": {
        "leads_target": 10,
        "calls_target": 4,
        "audits_target": 3,
        "builds_target": 2,
        "retainer_target": 1
    },
    "next_actions": [
        {"task": "Follow up with 3 warm leads", "priority": "HIGH", "agent": "Karma"},
        {"task": "Check Calendly for new bookings", "priority": "HIGH", "agent": "Yuki"},
        {"task": "Prepare audit deck for 2 pending leads", "priority": "MED", "agent": "Connor"},
        {"task": "Update EMVY landing page", "priority": "MED", "agent": "Emmy"},
    ]
}

# ─── LOAD DATA ────────────────────────────────────────────────────────────────

def load_data():
    state_file = Path("/home/dusk/.openclaw/shared/state/emvy-data.json")
    try:
        if state_file.exists():
            with open(state_file) as f:
                return json.load(f)
    except Exception:
        pass
    return FALLBACK_DATA

data = load_data()

# ─── HEADER ──────────────────────────────────────────────────────────────────

st.title("💰 EMVY Audit Dashboard")
st.caption(f"Last updated: {datetime.now(AWST_TZ).strftime('%Y-%m-%d %H:%M AWST')}")

st.divider()

# ─── KPI ROW ─────────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Leads", data["leads"]["total"], f"+{data['leads']['new_today']} today")

with col2:
    st.metric("Emails Sent", data["emails"]["sent"], f"{data['emails']['open_rate']} open rate")

with col3:
    st.metric("Calendly Bookings", data["calendly"]["booked"], f"{data['calendly']['upcoming']} upcoming")

with col4:
    st.metric("Monthly Revenue", f"${data['revenue']['monthly_recurring']:,}", f"Target: ${data['revenue']['target_monthly']:,}")

st.divider()

# ─── MAIN FUNNEL ─────────────────────────────────────────────────────────────

st.subheader("🎯 Revenue Funnel")

funnel = data["funnel"]
cols = st.columns(7)

steps = [
    ("Leads", funnel["leads"], "📧"),
    ("Contacted", funnel["contacted"], "📨"),
    ("Interested", funnel["interested"], "🙋"),
    ("Booked", funnel["booked"], "📅"),
    ("Audit Started", funnel["audit_started"], "🔍"),
    ("Build Started", funnel["build_started"], "🔨"),
    ("Retainer", funnel["retainer"], "💎"),
]

for i, (col, (label, count, emoji)) in enumerate(zip(cols, steps)):
    with col:
        st.metric(emoji, count, label)

# Funnel visualization
st.progress(funnel["retainer"] / max(funnel["leads"], 1), text=f"Conversion: {funnel['retainer']}/{funnel['leads']} leads → retainer ({funnel['retainer']/max(funnel['leads'],1)*100:.1f}%)")

st.divider()

# ─── LEADS SECTION ───────────────────────────────────────────────────────────

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Lead Sources")
    
    # Industry breakdown
    industries = data["leads"]["by_industry"]
    industry_data = sorted(industries.items(), key=lambda x: x[1], reverse=True)
    
    for industry, count in industry_data:
        pct = count / data["leads"]["total"] * 100
        st.write(f"{industry}: {count} ({pct:.0f}%)")
        st.progress(pct / 100, text="")

with col_right:
    st.subheader("📈 Email Campaign")
    
    email_stats = data["emails"]
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric("Delivered", email_stats["delivered"])
        st.metric("Opened", email_stats["opened"])
    
    with col_b:
        st.metric("Replied", email_stats["replied"])
        st.metric("Failed", email_stats["failed"])
    
    st.write(f"**Open Rate:** {email_stats['open_rate']}")
    st.write(f"**Reply Rate:** {email_stats['reply_rate']}")
    st.write(f"**Pending:** {email_stats['pending']}")

st.divider()

# ─── AUDIT PIPELINE ─────────────────────────────────────────────────────────

st.subheader("🔍 Audit Pipeline")

audit_cols = st.columns(4)

with audit_cols[0]:
    st.metric("In Progress", data["audits"]["in_progress"])

with audit_cols[1]:
    st.metric("Completed", data["audits"]["completed"])

with audit_cols[2]:
    st.metric("Pending Payment", data["audits"]["pending_payment"])

with audit_cols[3]:
    st.metric("Upgraded to Build", data["audits"]["upgraded_to_build"])

st.divider()

# ─── REVENUE TRACKER ─────────────────────────────────────────────────────────

st.subheader("💎 Revenue Tracker")

rev_cols = st.columns(4)

with rev_cols[0]:
    st.metric("Audit Revenue", f"${data['revenue']['audits_total']:,}")

with rev_cols[1]:
    st.metric("Build Revenue", f"${data['revenue']['builds_total']:,}")

with rev_cols[2]:
    st.metric("Retainer Revenue", f"${data['revenue']['retainers_total']:,}")

with rev_cols[3]:
    st.metric("Monthly MRR", f"${data['revenue']['monthly_recurring']:,}")

# Progress to targets
st.write("**Progress to Targets:**")
col_t1, col_t2 = st.columns(2)

with col_t1:
    progress_monthly = data["revenue"]["monthly_recurring"] / data["revenue"]["target_monthly"]
    st.progress(min(progress_monthly, 1.0), text=f"Monthly Target: ${data['revenue']['monthly_recurring']:,} / ${data['revenue']['target_monthly']:,}")

with col_t2:
    progress_quarterly = (data["revenue"]["monthly_recurring"] * 3) / data["revenue"]["target_quarterly"]
    st.progress(min(progress_quarterly, 1.0), text=f"Q2 Target: ${data['revenue']['monthly_recurring'] * 3:,} / ${data['revenue']['target_quarterly']:,}")

st.divider()

# ─── KPIs ───────────────────────────────────────────────────────────────────

st.subheader("🎯 Monthly KPIs")

kpis = data["kpis"]
kpi_cols = st.columns(5)

kpi_data = [
    ("Leads", data["leads"]["total"], kpis["leads_target"]),
    ("Discovery Calls", data["calendly"]["booked"], kpis["calls_target"]),
    ("Audits", data["audits"]["completed"], kpis["audits_target"]),
    ("Builds", data["audits"]["upgraded_to_build"], kpis["builds_target"]),
    ("Retainers", data["funnel"]["retainer"], kpis["retainer_target"]),
]

for col, (label, current, target) in zip(kpi_cols, kpi_data):
    with col:
        pct = current / target * 100 if target > 0 else 0
        st.metric(label, f"{current}/{target}", f"{pct:.0f}%")
        st.progress(min(current/target, 1.0) if target > 0 else 0)

st.divider()

# ─── NEXT ACTIONS ────────────────────────────────────────────────────────────

st.subheader("⚡ Next Actions")

actions = data.get("next_actions", [])
if actions:
    for action in actions:
        priority_color = "🔴" if action["priority"] == "HIGH" else "🟡" if action["priority"] == "MED" else "🟢"
        st.write(f"{priority_color} **{action['agent']}:** {action['task']}")
else:
    st.info("No pending actions")

st.divider()

# ─── PRICING REFERENCE ──────────────────────────────────────────────────────

st.subheader("💵 EMVY Pricing")

price_cols = st.columns(4)

prices = [
    ("AI Audit", "$1,500", "one-time"),
    ("Setup + Build", "$3,000-5,000", "project"),
    ("Monthly Retainer", "$1,500", "/month"),
    ("Enterprise", "$5,000", "/month"),
]

for col, (name, price, freq) in zip(price_cols, prices):
    with col:
        st.metric(name, price, freq)

st.divider()

# ─── CALENDLY LINK ──────────────────────────────────────────────────────────

st.markdown("### 📅 Book Free AI Chat")
st.markdown("[calendly.com/emvyai/free-ai-chat](https://calendly.com/emvyai/free-ai-chat)")
st.markdown("*15-min free call — no pressure, just see if we're a fit*")

st.divider()

# ─── FOOTER ─────────────────────────────────────────────────────────────────

st.caption("EMVY AI Audit Dashboard — Built by Yuki | Shut Up and Build 🚀")
