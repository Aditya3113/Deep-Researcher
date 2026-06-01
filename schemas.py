"""
Pydantic schemas used as structured output types throughout the pipeline.
"""

from pydantic import BaseModel, Field


class WebSearchItem(BaseModel):
    """A single planned web search, with the agent's reasoning."""

    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(
        description="The search term to use for the web search."
    )


class WebSearchPlan(BaseModel):
    """The full set of web searches the planner wants to perform."""

    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


class ReportData(BaseModel):
    """The structured output produced by the writer agent."""

    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )
    markdown_report: str = Field(
        description="The full detailed report in Markdown format."
    )
    follow_up_questions: list[str] = Field(
        description="Suggested topics or questions to research further."
    )
