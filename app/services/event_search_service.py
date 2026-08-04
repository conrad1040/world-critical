from sqlalchemy import or_, select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.events_service import (
    PUBLIC_PRIORITIES,
    serialize_event,
)

MIN_QUERY_LENGTH = 2
MAX_QUERY_LENGTH = 200

SEARCHABLE_PRIORITIES = PUBLIC_PRIORITIES


def _escape_like(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def search_events(query: str) -> dict:
    normalized_query = query.strip()[:MAX_QUERY_LENGTH]

    if len(normalized_query) < MIN_QUERY_LENGTH:
        return {
            "query": normalized_query,
            "results": [],
        }

    pattern = f"%{_escape_like(normalized_query)}%"

    with SessionLocal() as session:
        events = session.scalars(
            select(Event)
            .where(
                Event.editorial_priority.in_(
                    SEARCHABLE_PRIORITIES
                ),
                or_(
                    Event.title.ilike(
                        pattern,
                        escape="\\",
                    ),
                    Event.summary.ilike(
                        pattern,
                        escape="\\",
                    ),
                    Event.latest_development.ilike(
                        pattern,
                        escape="\\",
                    ),
                ),
            )
            .order_by(Event.importance_score.desc())
        ).all()

        return {
            "query": normalized_query,
            "results": [
                serialize_event(event)
                for event in events
            ],
        }
