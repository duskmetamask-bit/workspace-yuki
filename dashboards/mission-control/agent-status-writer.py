#!/usr/bin/env python3
"""
agent-status-writer.py
======================
Updates the shared agent-status.json file.
Agents call this at start and finish of their cron runs.

Usage:
    python agent-status-writer.py --agent harold --status ok \
        --action "18 searches complete — SMB industry deep dive" \
        --next-run "2026-04-07T08:00:00+08:00"

    python agent-status-writer.py --agent yuki --status running \
        --task "Reviewing Harold's research"

    python agent-status-writer.py --agent karma --status error \
        --action "Gmail API rate limit hit"
"""

import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_FILE = Path("/home/dusk/.openclaw/shared/state/agent-status.json")
AWST_TZ = timezone(timedelta(hours=8))


def load_state():
    """Load existing state or return default structure."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {
        "last_updated": datetime.now(AWST_TZ).isoformat(),
        "agents": {},
        "emvy": {},
        "upcoming_crons": []
    }


def save_state(state):
    """Write state to file atomically."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    tmp.rename(STATE_FILE)


def update_agent(agent_name, status=None, action=None, task=None, 
                 next_run=None, error_msg=None):
    """Update a single agent's status in the shared state."""
    state = load_state()
    
    if agent_name not in state["agents"]:
        state["agents"][agent_name] = {
            "status": "idle",
            "last_run": datetime.now(AWST_TZ).isoformat(),
            "last_action": "",
            "current_task": "",
        }
    
    agent = state["agents"][agent_name]
    
    if status:
        agent["status"] = status
    if action:
        agent["last_action"] = action
        agent["last_run"] = datetime.now(AWST_TZ).isoformat()
    if task:
        agent["current_task"] = task
    if next_run:
        agent["next_run"] = next_run
    if error_msg:
        agent["last_action"] = f"ERROR: {error_msg}"
        agent["status"] = "error"
    
    state["last_updated"] = datetime.now(AWST_TZ).isoformat()
    save_state(state)
    print(f"✅ Updated {agent_name}: status={agent['status']}, action={agent['last_action']}")


def update_emvy(leads_total=None, leads_new_today=None, emails_sent_today=None,
                emails_pending=None, bookings=None, audits_in_progress=None):
    """Update EMVY pipeline stats."""
    state = load_state()
    
    if "emvy" not in state:
        state["emvy"] = {}
    
    emvy = state["emvy"]
    if leads_total is not None:
        emvy["leads_total"] = leads_total
    if leads_new_today is not None:
        emvy["leads_new_today"] = leads_new_today
    if emails_sent_today is not None:
        emvy["emails_sent_today"] = emails_sent_today
    if emails_pending is not None:
        emvy["emails_pending"] = emails_pending
    if bookings is not None:
        emvy["bookings"] = bookings
    if audits_in_progress is not None:
        emvy["audits_in_progress"] = audits_in_progress
    
    state["last_updated"] = datetime.now(AWST_TZ).isoformat()
    save_state(state)
    print(f"✅ Updated EMVY: {emvy}")


def add_cron(name, agent, next_run):
    """Add or update a scheduled cron."""
    state = load_state()
    
    # Check if exists
    found = False
    for cron in state.get("upcoming_crons", []):
        if cron["name"] == name:
            cron["next_run"] = next_run
            found = True
            break
    
    if not found:
        state.setdefault("upcoming_crons", []).append({
            "name": name,
            "agent": agent,
            "next_run": next_run
        })
    
    state["last_updated"] = datetime.now(AWST_TZ).isoformat()
    save_state(state)
    print(f"✅ Updated cron: {name} → {next_run}")


def main():
    parser = argparse.ArgumentParser(description="Update agent status in Mission Control")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Agent update
    agent_parser = subparsers.add_parser("agent", help="Update agent status")
    agent_parser.add_argument("--agent", required=True, help="Agent name (e.g. harold)")
    agent_parser.add_argument("--status", required=True, 
                              choices=["ok", "idle", "running", "error"],
                              help="Current status")
    agent_parser.add_argument("--action", help="What the agent just did")
    agent_parser.add_argument("--task", help="Current task (for running agents)")
    agent_parser.add_argument("--next-run", help="ISO timestamp of next scheduled run")
    agent_parser.add_argument("--error", help="Error message (sets status to error)")
    
    # EMVY update
    emvy_parser = subparsers.add_parser("emvy", help="Update EMVY pipeline stats")
    emvy_parser.add_argument("--leads-total", type=int)
    emvy_parser.add_argument("--leads-new-today", type=int)
    emvy_parser.add_argument("--emails-sent-today", type=int)
    emvy_parser.add_argument("--emails-pending", type=int)
    emvy_parser.add_argument("--bookings", type=int)
    emvy_parser.add_argument("--audits-in-progress", type=int)
    
    # Cron update
    cron_parser = subparsers.add_parser("cron", help="Add/update scheduled cron")
    cron_parser.add_argument("--name", required=True, help="Cron name")
    cron_parser.add_argument("--agent", required=True, help="Agent name")
    cron_parser.add_argument("--next-run", required=True, help="ISO timestamp")
    
    args = parser.parse_args()
    
    if args.command == "agent":
        update_agent(
            agent_name=args.agent,
            status=args.status,
            action=args.action,
            task=args.task,
            next_run=args.next_run,
            error_msg=args.error
        )
    elif args.command == "emvy":
        update_emvy(
            leads_total=args.leads_total,
            leads_new_today=args.leads_new_today,
            emails_sent_today=args.emails_sent_today,
            emails_pending=args.emails_pending,
            bookings=args.bookings,
            audits_in_progress=args.audits_in_progress
        )
    elif args.command == "cron":
        add_cron(name=args.name, agent=args.agent, next_run=args.next_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
