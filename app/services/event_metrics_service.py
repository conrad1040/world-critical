from sqlalchemy import distinct, func, select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source


def update_event_metrics() -> int:
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

        for event in events:
            article_count = session.scalar(
                select(func.count(Article.id)).where(
                    Article.event_id == event.id
                )
            )

            source_count = session.scalar(
                select(func.count(distinct(Source.id)))
                .join(Article, Article.source_id == Source.id)
                .where(Article.event_id == event.id)
            )

            event.article_count = article_count or 0
            event.source_count = source_count or 0
            updated_count += 1

        session.commit()

    return updated_count