import app.models

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event


PUBLIC_PRIORITIES = ("Critical", "Watch")


def serialize_event(event: Event) -> dict:
    return {
        "id": event.id,
        "title": event.title,
        "summary": event.summary,
        "latest_development": event.latest_development,
        "category": event.category,
        "importance_score": event.importance_score,
        "article_count": event.article_count,
        "source_count": event.source_count,
        "status": event.status,
        "editorial_priority": event.editorial_priority,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
    }


def get_events() -> dict:
    with SessionLocal() as session:
        critical_events = session.scalars(
            select(Event)
            .where(Event.homepage_section == "critical")
            .order_by(
                Event.briefing_rank.desc(),
                Event.updated_at.desc(),
            )
        ).all()

        watch_events = session.scalars(
            select(Event)
            .where(Event.homepage_section == "watch")
            .order_by(
                Event.briefing_rank.desc(),
                Event.updated_at.desc(),
            )
        ).all()

        return {
            "critical": [
                serialize_event(event)
                for event in critical_events
            ],
            "watch": [
                serialize_event(event)
                for event in watch_events
            ],
        }