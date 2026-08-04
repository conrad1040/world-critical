import re


def clean_title(title: str) -> str:
    """
    Clean a news headline for use as an event title.
    """

    # Remove source after " - "
    title = re.sub(r"\s-\s.*$", "", title)

    # Remove source after " | "
    title = re.sub(r"\s\|.*$", "", title)

    # Collapse extra whitespace
    title = " ".join(title.split())

    return title.strip()


def create_event_title(article_title: str) -> str:
    """
    Create an initial event title from an article title.
    This is only used when the event is first created.
    The AI will later refine the title as the event evolves.
    """
    return clean_title(article_title)


def create_event_summary(article_title: str) -> str:
    """
    Create a placeholder summary until the AI generates
    the first full event briefing.
    """
    title = clean_title(article_title)

    return (
        f"{title}. "
        "This event is being tracked by World Critical as "
        "additional reporting becomes available."
    )