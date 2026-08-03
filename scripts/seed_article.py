from datetime import datetime, timezone

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.source import Source
from app.models.event import Event


def main() -> None:
    with SessionLocal() as session:
        source = Source(
            name="Example News",
            website="https://example.com",
            country="United States",
        )
        session.add(source)
        session.flush()

        article = Article(
            title="World Critical stores its first article",
            url="https://example.com/world-critical-first-article",
            published_at=datetime.now(timezone.utc).replace(tzinfo=None),
            source_id=source.id,
            event_id=None,
        )
        session.add(article)
        session.commit()

        print(f"Created source ID {source.id} and article ID {article.id}")


if __name__ == "__main__":
    main()