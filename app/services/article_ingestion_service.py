from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.source import Source
from app.services.news_service import fetch_world_news


def _parse_published_at(value: str) -> datetime:
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).replace(tzinfo=None)


def _get_website_url(article_url: str) -> str:
    parsed_url = urlparse(article_url)

    if not parsed_url.scheme or not parsed_url.netloc:
        return article_url

    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def ingest_top_headlines(
    page_size: int = 50,
) -> int:
    """
    Ingest broad World Critical news discovery results.

    The function name is preserved so scripts that already call
    ingest_top_headlines() do not need to change yet.
    """
    news_items = fetch_world_news(page_size=page_size)
    created_count = 0

    with SessionLocal() as session:
        incoming_urls = {
            item.get("url")
            for item in news_items
            if item.get("url")
        }

        existing_urls: set[str] = set()

        if incoming_urls:
            existing_urls = set(
                session.scalars(
                    select(Article.url).where(
                        Article.url.in_(incoming_urls)
                    )
                ).all()
            )

        source_cache: dict[str, Source] = {}

        for item in news_items:
            url = item.get("url")
            title = item.get("title")
            published_at = item.get("publishedAt")
            source_name = item.get("source", {}).get("name")

            if (
                not url
                or not title
                or not published_at
                or not source_name
            ):
                continue

            if url in existing_urls:
                continue

            source = source_cache.get(source_name)

            if source is None:
                source = session.scalar(
                    select(Source).where(
                        Source.name == source_name
                    )
                )

                if source is None:
                    source = Source(
                        name=source_name,
                        website=_get_website_url(url),
                        country=None,
                    )
                    session.add(source)
                    session.flush()

                source_cache[source_name] = source

            try:
                published_datetime = _parse_published_at(
                    published_at
                )
            except ValueError:
                print(
                    "Skipping article with invalid publication "
                    f"date: {title}"
                )
                continue

            article = Article(
                title=title,
                url=url,
                published_at=published_datetime,
                source_id=source.id,
                event_id=None,
            )

            session.add(article)
            existing_urls.add(url)
            created_count += 1

        session.commit()

    return created_count