"""
Search agent — runs a single web search and returns a concise summary.
"""

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings
from config import SEARCH_MODEL, SEARCH_CONTEXT_SIZE

_INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than "
    "300 words. Capture the main points. Write succinctly — no need for complete sentences or "
    "polished grammar. This will be consumed by someone synthesizing a report, so it is vital "
    "you capture the essence and ignore any fluff. Do not include any additional commentary "
    "other than the summary itself."
)

search_agent = Agent(
    name="SearchAgent",
    instructions=_INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size=SEARCH_CONTEXT_SIZE)],
    model=SEARCH_MODEL,
    model_settings=ModelSettings(tool_choice="required"),
)
