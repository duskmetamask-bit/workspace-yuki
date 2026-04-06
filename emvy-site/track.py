#!/usr/bin/env python3
"""Simple click tracker — logs hits and redirects to Calendly."""
import os
from datetime import datetime

LOG_FILE = "/home/dusk/.openclaw/workspace-yuki/emvy-site/clicks.log"

def log_click():
    ts = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts}\n")

# Log the hit
log_click()

# Output a minimal HTML redirect to Calendly
print("Content-Type: text/html")
print("Location: https://calendly.com/emvyai/free-ai-chat")
print()
print("<html><head><meta http-equiv='refresh' content='0;url=https://calendly.com/emvyai/free-ai-chat'></head><body>Redirecting...</body></html>")
