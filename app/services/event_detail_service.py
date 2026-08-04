from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source
from app.services.events_service import PUBLIC_PRIORITIES


def get_event(event_id: int) -> dict | None:
    with SessionLocal() as session:
        event = session.get(Event, event_id)

        if event is None:
            return None

        if event.editorial_priority not in PUBLIC_PRIORITIES:
            return None

        articles = session.scalars(
            select(Article)
            .where(Article.event_id == event.id)
            .order_by(Article.published_at.desc())
        ).all()

        article_list = []

        sources = set()

        for article in articles:
            source = session.get(Source, article.source_id)

            if source:
                sources.add(source.name)

            article_list.append(
                {
                    "title": article.title,
                    "url": article.url,
                    "published_at": article.published_at.isoformat(),
                    "source": source.name if source else "Unknown",
                }
            )

        return {
            "id": event.id,
            "title": event.title,
            "summary": event.summary,
            "latest_development": event.latest_development,
            "why_it_matters": event.why_it_matters,
            "what_happens_next": event.what_happens_next,
            "impact_scope": event.impact_scope,
            "confidence": event.confidence,
            "homepage": event.homepage,
            "category": event.category,
            "importance_score": event.importance_score,
            "status": event.status,
            "article_count": event.article_count,
            "source_count": event.source_count,
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat(),
            "sources": sorted(sources),
            "articles": article_list,
            "editorial_priority": event.editorial_priority,
        }