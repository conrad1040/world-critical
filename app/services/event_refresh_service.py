from sqlalchemy import func, select

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
            select(Event).where(
                Event.needs_refresh.is_(True)
            )
        ).all()

        for event in events:
            new_articles = session.scalars(
                select(Article)
                .where(
                    Article.event_id == event.id,
                    Article.processed_for_event.is_(False),
                )
                .order_by(Article.published_at)
            ).all()

            if not new_articles:
                event.needs_refresh = False
                continue

            new_articles_payload = [
                {
                    "title": article.title,
                    "description": article.description or "",
                }
                for article in new_articles
            ]

            print(f"Evaluating event {event.id}...")

            evaluation = evaluate_event(
                current_summary=event.summary,
                current_latest_development=event.latest_development,
                current_why_it_matters=event.why_it_matters,
                current_what_happens_next=event.what_happens_next,
                new_articles=new_articles_payload,
                source_count=event.source_count,
                article_count=event.article_count,
                category=event.category,
                importance_score=event.importance_score,
            )

            recommended_priority = evaluation[
                "editorial_priority"
            ]

            final_priority = apply_editorial_rules(
                recommended_priority=recommended_priority,
                confidence=evaluation["confidence"],
                source_count=event.source_count,
            )

            event.summary = evaluation["summary"]
            event.latest_development = evaluation[
                "latest_development"
            ]
            event.why_it_matters = evaluation[
                "why_it_matters"
            ]
            event.what_happens_next = evaluation[
                "what_happens_next"
            ]
            event.impact_scope = evaluation[
                "impact_scope"
            ]
            event.confidence = evaluation["confidence"]
            event.editorial_priority = final_priority

            latest_published = max(
                article.published_at
                for article in new_articles
            )

            all_latest = session.scalar(
                select(func.max(Article.published_at)).where(
                    Article.event_id == event.id
                )
            )

            if all_latest is not None:
                event.updated_at = all_latest
            else:
                event.updated_at = latest_published

            event.needs_refresh = False

            for article in new_articles:
                article.processed_for_event = True

            updated_count += 1

            print(
                f"Event {event.id}: "
                f"recommended={recommended_priority}, "
                f"final={final_priority} — "
                f"{evaluation['reasoning']}"
            )

        session.commit()

    return updated_count