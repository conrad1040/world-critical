import app.models

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event


def get_events() -> list[dict]:
    with SessionLocal() as session:
        events = session.scalars(
            select(Event)
            .where(Event.status == "Qualifying")
            .order_by(Event.importance_score.desc())
        ).all()

        return [
            {
                "id": event.id,
                "title": event.title,
                "summary": event.summary,
                "category": event.category,
                "importance_score": event.importance_score,
                "article_count": event.article_count,
                "source_count": event.source_count,
                "status": event.status,
                "created_at": event.created_at.isoformat(),
                "updated_at": event.updated_at.isoformat(),
            }
            for event in events
        ]