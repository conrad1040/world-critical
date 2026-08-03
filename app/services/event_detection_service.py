from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.services.event_matching_service import titles_match
from app.services.event_text_service import (
    create_event_summary,
    create_event_title,
)


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
                    title=create_event_title(article.title),
                    summary=create_event_summary(article.title),
                    importance_score=0,
                    status="Candidate",
                    needs_refresh=True,
                )

                session.add(matched_event)
                session.flush()

                events.append(matched_event)
                created_count += 1

            article.event_id = matched_event.id
            matched_event.needs_refresh = True

        session.commit()

    return created_count