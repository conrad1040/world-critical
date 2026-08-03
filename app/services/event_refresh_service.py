from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.services.editor_service import evaluate_event


def apply_editorial_rules(
    recommended_priority: str,
    confidence: str,
    source_count: int,
) -> str:
    final_priority = recommended_priority

    # Never allow a single-source story directly onto the main briefing.
    if (
        recommended_priority == "Critical"
        and source_count < 2
    ):
        final_priority = "Watch"

    return final_priority


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

            print(f"Evaluating event {event.id}...")

            evaluation = evaluate_event(
                headlines=article_titles,
                source_count=event.source_count,
                article_count=event.article_count,
                category=event.category,
                importance_score=event.importance_score,
            )

            recommended_priority = evaluation["editorial_priority"]

            final_priority = apply_editorial_rules(
                recommended_priority=recommended_priority,
                confidence=evaluation["confidence"],
                source_count=event.source_count,
            )

            event.summary = evaluation["summary"]
            event.why_it_matters = evaluation["why_it_matters"]
            event.what_happens_next = evaluation["what_happens_next"]
            event.impact_scope = evaluation["impact_scope"]
            event.confidence = evaluation["confidence"]
            event.editorial_priority = final_priority

            # The application controls what enters the main briefing.
            event.homepage = final_priority == "Critical"

            event.needs_refresh = False
            updated_count += 1

            print(
                f"Event {event.id}: "
                f"recommended={recommended_priority}, "
                f"final={final_priority} — "
                f"{evaluation['reasoning']}"
            )

            session.commit()

    return updated_count