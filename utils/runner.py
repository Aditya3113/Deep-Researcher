"""
Pipeline runner — orchestrates the full deep-research workflow:

  1. plan_searches   → planner_agent decides which queries to run
  2. perform_searches → search_agent runs them in parallel
  3. write_report    → writer_agent synthesises a Markdown report
  4. email_report    → email_agent sends the report via SendGrid (optional)
"""

import asyncio

from agents import Runner, trace

from agents.planner  import planner_agent
from agents.searcher import search_agent
from agents.writer   import writer_agent
from agents.emailer  import email_agent
from schemas import WebSearchItem, WebSearchPlan, ReportData


# ── Step 1: Planning ──────────────────────────────────────────────────────────

async def plan_searches(query: str) -> WebSearchPlan:
    """Ask the planner agent which searches to run."""
    print("📋  Planning searches...")
    result = await Runner.run(planner_agent, f"Query: {query}")
    plan: WebSearchPlan = result.final_output
    print(f"    → Will perform {len(plan.searches)} searches")
    for i, item in enumerate(plan.searches, 1):
        print(f"       {i}. {item.query!r}  ({item.reason[:60]}...)")
    return plan


# ── Step 2: Searching ─────────────────────────────────────────────────────────

async def _search_one(item: WebSearchItem) -> str:
    """Run one web search and return the summary text."""
    user_input = f"Search term: {item.query}\nReason for searching: {item.reason}"
    result = await Runner.run(search_agent, user_input)
    return result.final_output


async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
    """Run all planned searches concurrently."""
    print("🔍  Searching the web (parallel)...")
    tasks = [asyncio.create_task(_search_one(item)) for item in search_plan.searches]
    results = await asyncio.gather(*tasks)
    print("    → All searches complete")
    return list(results)


# ── Step 3: Report writing ────────────────────────────────────────────────────

async def write_report(query: str, search_results: list[str]) -> ReportData:
    """Synthesise search summaries into a detailed report."""
    print("✍️   Writing report...")
    user_input = (
        f"Original query: {query}\n"
        f"Summarized search results:\n"
        + "\n\n---\n\n".join(search_results)
    )
    result = await Runner.run(writer_agent, user_input)
    report: ReportData = result.final_output
    print("    → Report written")
    return report


# ── Step 4: Email delivery ────────────────────────────────────────────────────

async def email_report(report: ReportData) -> ReportData:
    """Convert the report to HTML and email it."""
    print("📧  Sending email...")
    await Runner.run(email_agent, report.markdown_report)
    print("    → Email sent")
    return report


# ── Full pipeline ─────────────────────────────────────────────────────────────

async def run_pipeline(query: str, send_email: bool = True) -> ReportData:
    """
    Run the complete deep-research pipeline.

    Args:
        query:      The research question / topic.
        send_email: Whether to email the finished report (requires SendGrid).

    Returns:
        A ReportData object containing the report and metadata.
    """
    with trace("DeepResearch"):
        print(f"\n🚀  Starting deep research for: {query!r}\n")

        search_plan    = await plan_searches(query)
        search_results = await perform_searches(search_plan)
        report         = await write_report(query, search_results)

        if send_email:
            await email_report(report)

        print("\n✅  Done!\n")
        return report
