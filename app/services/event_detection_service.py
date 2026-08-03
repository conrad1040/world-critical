from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source
from app.services.event_matching_service import titles_match


def detect_events() -> int:
    created_count = 0

    with SessionLocal() as session:
        articles = session.scalars(
            select(Article).where(Article.event_id.is_(None))
        ).all()

        events = session.scalars(select(Event)).all()

        for article in articles:
            matched_event = next(
                (
                    event
                    for event in events
                    if titles_match(article.title, event.title)
                ),
                None,
            )

            if matched_event is None:
                matched_event = Event(
                    title=article.title,
                    summary=article.title,
                    importance_score=0,
                    status="Candidate",
                )
                session.add(matched_event)
                session.flush()

                events.append(matched_event)
                created_count += 1

            article.event_id = matched_event.id

        session.commit()

    return created_count