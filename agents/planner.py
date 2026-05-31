"""
Planner agent — decides which web searches to run for a given query.
"""

from agents import Agent
from schemas import WebSearchPlan
from config import PLANNER_MODEL, HOW_MANY_SEARCHES

_INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=_INSTRUCTIONS,
    model=PLANNER_MODEL,
    output_type=WebSearchPlan,
)
