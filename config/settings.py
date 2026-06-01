"""
Configuration settings for the Deep Researcher project.
Update these values before running.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ── Model settings ────────────────────────────────────────────────────────────
PLANNER_MODEL = "gpt-4o-mini"
SEARCH_MODEL  = "gpt-4o-mini"
WRITER_MODEL  = "gpt-4o-mini"
EMAIL_MODEL   = "gpt-4o-mini"

# ── Search settings ───────────────────────────────────────────────────────────
HOW_MANY_SEARCHES = 3          # Number of parallel web searches to perform
SEARCH_CONTEXT_SIZE = "low"    # "low" | "medium" | "high"  (affects cost)

# ── Email settings ────────────────────────────────────────────────────────────
# Set these via environment variables, or hard-code for local dev only
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL       = os.getenv("FROM_EMAIL", "you@example.com")   # Must be verified in SendGrid
TO_EMAIL         = os.getenv("TO_EMAIL",   "you@example.com")

# ── Report settings ───────────────────────────────────────────────────────────
REPORT_MIN_WORDS = 1000   # Target minimum word count for the final report
