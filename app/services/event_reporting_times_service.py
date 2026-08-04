from datetime import datetime

from sqlalchemy import func, select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event


def sync_event_reporting_times() -> int:
    """
    Align event created_at / updated_at with article publication times.

    created_at -> earliest linked article published_at (first reported)
    updated_at -> latest linked article published_at (last new reporting)
    """
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

        for event in events:
            earliest = session.scalar(
                select(func.min(Article.published_at)).where(
                    Article.event_id == event.id
                )
            )

            latest = session.scalar(
                select(func.max(Article.published_at)).where(
                    Article.event_id == event.id
                )
            )

            if earliest is None or latest is None:
                continue

            event.created_at = earliest
            event.updated_at = latest
            updated_count += 1

        session.commit()

    return updated_count
