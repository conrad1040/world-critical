from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event


def get_events():
    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

        return [
            {
                "id": event.id,
                "title": event.title,
                "summary": event.summary,
                "importance_score": event.importance_score,
                "status": event.status,
                "created_at": event.created_at.isoformat(),
            }
            for event in events
        ]