from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.event import Event
from app.services.openai_service import (
    generate_event_merge_decision,
)


def should_merge_events(
    event_a_title: str,
    event_a_summary: str,
    event_b_title: str,
    event_b_summary: str,
) -> dict[str, str | bool]:
    """
    Decide whether two events actually represent
    the same evolving real-world event.
    """

    return generate_event_merge_decision(
        event_a_title=event_a_title,
        event_a_summary=event_a_summary,
        event_b_title=event_b_title,
        event_b_summary=event_b_summary,
    )


def merge_events(
    session: Session,
    keep_event: Event,
    remove_event: Event,
) -> None:
    """
    Merge two events.

    All articles from remove_event are reassigned to keep_event.
    The duplicate event is then deleted.

    This function intentionally does NOT regenerate titles,
    summaries, metrics, or importance scores. Those are handled
    separately by the event refresh pipeline.
    """

    for article in remove_event.articles:
        article.event_id = keep_event.id

    session.delete(remove_event)
    session.flush()