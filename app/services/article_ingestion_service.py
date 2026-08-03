from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source
from app.services.news_service import fetch_top_headlines


def ingest_top_headlines(page_size: int = 5) -> int:
    headlines = fetch_top_headlines(page_size=page_size)
    created_count = 0

    with SessionLocal() as session:
        for item in headlines:
            url = item.get("url")
            title = item.get("title")
            published_at = item.get("publishedAt")
            source_name = item.get("source", {}).get("name")

            if not url or not title or not published_at or not source_name:
                continue

            existing_article = session.scalar(
                select(Article).where(Article.url == url)
            )
            if existing_article:
                continue

            source = session.scalar(
                select(Source).where(Source.name == source_name)
            )

            if source is None:
                source = Source(
                    name=source_name,
                    website=url,
                    country=None,
                )
                session.add(source)
                session.flush()

            article = Article(
                title=title,
                url=url,
                published_at=datetime.fromisoformat(
                    published_at.replace("Z", "+00:00")
                ).replace(tzinfo=None),
                source_id=source.id,
                event_id=None,
            )

            session.add(article)
            created_count += 1

        session.commit()

    return created_count