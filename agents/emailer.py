"""
Email agent — converts a Markdown report to HTML and sends it via SendGrid.
"""

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
