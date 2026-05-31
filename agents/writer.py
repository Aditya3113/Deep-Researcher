"""
Writer agent — synthesises search results into a detailed Markdown report.
"""

from agents import Agent
from schemas import ReportData
from config import WRITER_MODEL, REPORT_MIN_WORDS

_INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    f"The final output should be in Markdown format, and it should be lengthy and detailed. "
    f"Aim for 5-10 pages of content, at least {REPORT_MIN_WORDS} words."
)

writer_agent = Agent(
    name="WriterAgent",
    instructions=_INSTRUCTIONS,
    model=WRITER_MODEL,
    output_type=ReportData,
)
