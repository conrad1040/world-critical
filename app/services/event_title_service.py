from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.openai_service import generate_event_display_title


def refresh_homepage_event_titles() -> int:
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(
            select(Event)
            .where(Event.homepage_section.is_not(None))
            .order_by(Event.briefing_rank.desc())
        ).all()

        for event in events:
            print(f"Rewriting homepage title for event {event.id}...")

            new_title = generate_event_display_title(
                current_title=event.title,
                summary=event.summary,
                why_it_matters=event.why_it_matters,
                latest_development=event.latest_development,
            )

            event.title = new_title[:255]
            updated_count += 1

            safe_title = new_title.encode("ascii", "replace").decode("ascii")
            print(f"  -> {safe_title}")

        session.commit()

    return updated_count
