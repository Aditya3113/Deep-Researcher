# 🔬 Deep Researcher

A structured, multi-agent deep-research pipeline built with the **OpenAI Agents SDK**.

---

## Architecture

```
query (str)
    │
    ▼
┌──────────────┐        WebSearchPlan
│ PlannerAgent │──────────────────────┐
└──────────────┘                      │  (N searches planned)
                                      │
          ┌───────────────────────────┤
          │           │               │
          ▼           ▼               ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │SearchAgent│  │SearchAgent│  │SearchAgent│   (run in parallel)
    └───────────┘  └───────────┘  └───────────┘
          │           │               │
          └───────────┴───────────────┘
                      │  list[str] summaries
                      ▼
              ┌──────────────┐
              │ WriterAgent  │──→  ReportData (Markdown + metadata)
              └──────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  EmailAgent  │──→  HTML email via SendGrid
              └──────────────┘
```

---

## Project layout

```
deep_researcher/
│
├── agents/
│   ├── __init__.py       # Re-exports all four agents
│   ├── planner.py        # PlannerAgent  — decides which searches to run
│   ├── searcher.py       # SearchAgent   — runs a single web search
│   ├── writer.py         # WriterAgent   — synthesises search results into a report
│   └── emailer.py        # EmailAgent    — converts Markdown → HTML and sends it
│
├── utils/
│   ├── __init__.py
│   ├── runner.py         # Async orchestration: plan → search → write → email
│   └── display.py        # Pretty-print / Jupyter rendering helpers
│
├── config/
│   ├── __init__.py
│   └── settings.py       # All tuneable settings (models, counts, email addresses)
│
├── schemas.py            # Pydantic models: WebSearchItem, WebSearchPlan, ReportData
├── main.py               # CLI entry point
├── notebook.ipynb        # Interactive Jupyter notebook
├── requirements.txt
└── .env.example
```

---

## Quick start

```bash
# 1. Clone / copy the project
cd deep_researcher

# 2. Create a virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
cp .env.example .env
# Edit .env with your OPENAI_API_KEY, SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL

# 5. Run from the CLI
python main.py "Latest AI Agent frameworks in 2025"

# 6. Skip email (if SendGrid not configured)
python main.py "Latest AI Agent frameworks in 2025" --no-email
```

---

## Configuration

Edit `config/settings.py` or set environment variables in `.env`:

| Setting              | Default            | Description                          |
|----------------------|--------------------|--------------------------------------|
| `HOW_MANY_SEARCHES`  | `3`                | Number of parallel web searches      |
| `SEARCH_CONTEXT_SIZE`| `"low"`            | `low` / `medium` / `high` (cost ↑)  |
| `PLANNER_MODEL`      | `"gpt-4o-mini"`    | Model used by the planner            |
| `SEARCH_MODEL`       | `"gpt-4o-mini"`    | Model used by each search agent      |
| `WRITER_MODEL`       | `"gpt-4o-mini"`    | Model used by the writer             |
| `EMAIL_MODEL`        | `"gpt-4o-mini"`    | Model used by the email agent        |
| `REPORT_MIN_WORDS`   | `1000`             | Target minimum word count            |
| `FROM_EMAIL`         | —                  | SendGrid verified sender address     |
| `TO_EMAIL`           | —                  | Recipient email address              |

---

## Cost note

Each `WebSearchTool` call costs **~$0.025** on OpenAI (as of 2025).  
With `HOW_MANY_SEARCHES = 3`, a full pipeline run costs roughly **$0.08–$0.12**.

---

## Traces

All runs are traced via the OpenAI tracing SDK under the name `DeepResearch`.  
View them at: https://platform.openai.com/traces
