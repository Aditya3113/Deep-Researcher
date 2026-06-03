import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from agents import Agent, function_tool
from config import EMAIL_MODEL, SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an HTML email with the given subject and body via SendGrid."""
    if not SENDGRID_API_KEY:
        raise EnvironmentError(
            "SENDGRID_API_KEY is not set. "
            "Add it to your .env file or environment variables."
        )

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    mail = Mail(
        from_email=Email(FROM_EMAIL),
        to_emails=To(TO_EMAIL),
        subject=subject,
        html_content=Content("text/html", html_body),
    ).get()
    response = sg.client.mail.send.post(request_body=mail)

    status = response.status_code
    if status not in (200, 202):
        raise RuntimeError(f"SendGrid returned unexpected status: {status}")

    return {"status": "success", "http_status": str(status)}


_INSTRUCTIONS = (
    "You are able to send a nicely formatted HTML email based on a detailed report. "
    "You will be provided with a detailed report. You should use your tool to send one email, "
    "providing the report converted into clean, well-presented HTML with an appropriate subject line."
)

email_agent = Agent(
    name="EmailAgent",
    instructions=_INSTRUCTIONS,
    tools=[send_email],
    model=EMAIL_MODEL,
)


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
