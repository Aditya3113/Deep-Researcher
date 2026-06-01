"""
Display helpers — pretty-print a ReportData in Jupyter or plain terminal.
"""

from schemas import ReportData


def display_report(report: ReportData) -> None:
    """
    Render the report.  
    - In a Jupyter / IPython environment: renders Markdown.
    - Elsewhere: prints plain text to stdout.
    """
    try:
        from IPython.display import display, Markdown  # type: ignore
        display(Markdown(f"## Summary\n\n{report.short_summary}"))
        display(Markdown(report.markdown_report))
        display(Markdown("## Suggested follow-up questions"))
        for q in report.follow_up_questions:
            display(Markdown(f"- {q}"))
    except ImportError:
        _print_report(report)


def _print_report(report: ReportData) -> None:
    sep = "─" * 72

    print(f"\n{sep}")
    print("SUMMARY")
    print(sep)
    print(report.short_summary)

    print(f"\n{sep}")
    print("FULL REPORT")
    print(sep)
    print(report.markdown_report)

    print(f"\n{sep}")
    print("FOLLOW-UP QUESTIONS")
    print(sep)
    for q in report.follow_up_questions:
        print(f"  • {q}")
    print()
