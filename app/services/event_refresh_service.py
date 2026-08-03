from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.services.openai_service import generate_event_text


def refresh_event_text() -> int:
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(
            select(Event).where(Event.needs_refresh.is_(True))
        ).all()

        for event in events:
            articles = session.scalars(
                select(Article)
                .where(Article.event_id == event.id)
                .order_by(Article.published_at)
            ).all()

            if not articles:
                continue

            article_titles = [article.title for article in articles]

            print(f"Generating text for event {event.id}...")

            title, summary = generate_event_text(article_titles)

            event.title = title
            event.summary = summary
            event.needs_refresh = False
            updated_count += 1

            session.commit()

    return updated_count