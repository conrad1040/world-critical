from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.event_categorization_service import categorize_event
from app.models.article import Article
from app.models.source import Source

def update_event_categories() -> int:
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

        for event in events:
            event.category = categorize_event(event.title)
            updated_count += 1

        session.commit()

    return updated_count