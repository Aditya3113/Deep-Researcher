"""
main.py — CLI entry point for the Deep Researcher.

Usage:
    python main.py "Latest AI Agent frameworks in 2025"
    python main.py "Latest AI Agent frameworks in 2025" --no-email
"""

import argparse
import asyncio
import sys

from utils.runner import run_pipeline
from utils.display import display_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deep Researcher — multi-agent web research pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="Latest AI Agent frameworks in 2025",
        help="The research topic or question (default: AI Agent frameworks in 2025)",
    )
    parser.add_argument(
        "--no-email",
        dest="send_email",
        action="store_false",
        default=True,
        help="Skip emailing the report (useful when SendGrid is not configured)",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    report = await run_pipeline(query=args.query, send_email=args.send_email)
    display_report(report)


if __name__ == "__main__":
    asyncio.run(main())
