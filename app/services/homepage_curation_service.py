from sqlalchemy import select, update

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.events_service import PUBLIC_PRIORITIES
from app.services.openai_service import generate_homepage_curation

CRITICAL_CAP = 5
WATCH_CAP = 8


def _clear_homepage_selections(session) -> None:
    session.execute(
        update(Event).values(
            homepage_section=None,
            briefing_rank=None,
        )
    )


def _serialize_candidate(event: Event) -> dict[str, str | int | None]:
    return {
        "id": event.id,
        "title": event.title,
        "summary": event.summary,
        "latest_development": event.latest_development,
        "editorial_priority": event.editorial_priority,
        "category": event.category,
        "impact_scope": event.impact_scope,
        "confidence": event.confidence,
        "importance_score": event.importance_score,
        "source_count": event.source_count,
        "article_count": event.article_count,
    }


def _dedupe_by_macro_story(
    selections: list[dict[str, object]],
) -> list[dict[str, object]]:
    best_by_story: dict[str, dict[str, object]] = {}

    for selection in selections:
        event_id = int(selection["event_id"])
        briefing_rank = int(selection["briefing_rank"])
        macro_story = str(
            selection.get("macro_story") or f"event-{event_id}"
        ).strip().lower()

        existing = best_by_story.get(macro_story)

        if (
            existing is None
            or briefing_rank > int(existing["briefing_rank"])
        ):
            best_by_story[macro_story] = {
                "event_id": event_id,
                "briefing_rank": briefing_rank,
                "macro_story": macro_story,
            }

    return sorted(
        best_by_story.values(),
        key=lambda item: int(item["briefing_rank"]),
        reverse=True,
    )


def _apply_section_selections(
    session,
    section: str,
    selections: list[dict[str, object]],
    cap: int,
) -> int:
    applied = 0

    for selection in selections[:cap]:
        event = session.get(Event, int(selection["event_id"]))

        if event is None:
            continue

        event.homepage_section = section
        event.briefing_rank = int(selection["briefing_rank"])
        applied += 1

    return applied


def _fallback_curation(session) -> tuple[int, int]:
    critical_events = session.scalars(
        select(Event)
        .where(Event.editorial_priority == "Critical")
        .order_by(
            Event.importance_score.desc(),
            Event.updated_at.desc(),
        )
        .limit(CRITICAL_CAP)
    ).all()

    watch_events = session.scalars(
        select(Event)
        .where(Event.editorial_priority == "Watch")
        .order_by(
            Event.importance_score.desc(),
            Event.updated_at.desc(),
        )
        .limit(WATCH_CAP)
    ).all()

    critical_count = 0

    for rank, event in enumerate(critical_events, start=1):
        event.homepage_section = "critical"
        event.briefing_rank = 100 - rank
        critical_count += 1

    watch_count = 0

    for rank, event in enumerate(watch_events, start=1):
        event.homepage_section = "watch"
        event.briefing_rank = 100 - rank
        watch_count += 1

    return critical_count, watch_count


def curate_homepage() -> dict[str, int | str]:
    with SessionLocal() as session:
        _clear_homepage_selections(session)

        candidates = session.scalars(
            select(Event)
            .where(
                Event.editorial_priority.in_(
                    PUBLIC_PRIORITIES
                )
            )
            .order_by(Event.updated_at.desc())
        ).all()

        if not candidates:
            session.commit()
            return {
                "critical_count": 0,
                "watch_count": 0,
                "mode": "empty",
                "reasoning": "No candidate events.",
            }

        try:
            curation = generate_homepage_curation(
                candidates=[
                    _serialize_candidate(event)
                    for event in candidates
                ],
                critical_cap=CRITICAL_CAP,
                watch_cap=WATCH_CAP,
            )

            critical_selections = _dedupe_by_macro_story(
                curation.get("critical", [])
            )
            watch_selections = _dedupe_by_macro_story(
                curation.get("watch", [])
            )

            critical_count = _apply_section_selections(
                session,
                "critical",
                critical_selections,
                CRITICAL_CAP,
            )
            watch_count = _apply_section_selections(
                session,
                "watch",
                watch_selections,
                WATCH_CAP,
            )

            session.commit()

            reasoning = str(curation.get("reasoning", ""))

            print(f"Homepage curation: {reasoning}")

            return {
                "critical_count": critical_count,
                "watch_count": watch_count,
                "mode": "ai",
                "reasoning": reasoning,
            }

        except Exception as error:
            session.rollback()

            with SessionLocal() as fallback_session:
                _clear_homepage_selections(fallback_session)
                critical_count, watch_count = _fallback_curation(
                    fallback_session
                )
                fallback_session.commit()

            print(
                "Homepage curation fallback after error: "
                f"{error}"
            )

            return {
                "critical_count": critical_count,
                "watch_count": watch_count,
                "mode": "fallback",
                "reasoning": str(error),
            }
