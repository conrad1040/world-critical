from datetime import datetime, timezone

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source


def main() -> None:
    with SessionLocal() as session:
        source = session.scalar(
            select(Source).where(Source.name == "Test News")
        )

        if source is None:
            source = Source(
                name="Test News",
                website="https://testnews.example",
                country=None,
            )
            session.add(source)
            session.flush()

        article = Article(
            title="Explosion near Moscow cafe kills three - AP News",
            url="https://testnews.example/moscow-explosion",
            published_at=datetime.now(timezone.utc).replace(tzinfo=None),
            source_id=source.id,
            event_id=None,
        )

        session.add(article)
        session.commit()

        print(f"Created test article with ID {article.id}")


if __name__ == "__main__":
    main()
