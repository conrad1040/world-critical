import re


def clean_title(title: str) -> str:
    # Remove source after " - "
    title = re.sub(r"\s-\s.*$", "", title)

    # Remove source after " | "
    title = re.sub(r"\s\|.*$", "", title)

    # Collapse extra whitespace
    title = " ".join(title.split())

    return title.strip()


def create_event_title(article_title: str) -> str:
    return clean_title(article_title)


import re


def clean_title(title: str) -> str:
    # Remove source after " - "
    title = re.sub(r"\s-\s.*$", "", title)

    # Remove source after " | "
    title = re.sub(r"\s\|.*$", "", title)

    # Collapse extra whitespace
    title = " ".join(title.split())

    return title.strip()


def create_event_title(article_title: str) -> str:
    return clean_title(article_title)


def create_event_summary(article_title: str) -> str:
    title = clean_title(article_title)

    return (
        f"{title}. "
        "This event is being tracked by World Critical as additional "
        "reporting becomes available."
    )