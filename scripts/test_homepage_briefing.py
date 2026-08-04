from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.homepage_curation_service import (
    CRITICAL_CAP,
    WATCH_CAP,
)


def print_homepage_briefing_report() -> None:
    with SessionLocal() as session:
        critical_events = session.scalars(
            select(Event)
            .where(Event.homepage_section == "critical")
            .order_by(
                Event.briefing_rank.desc(),
                Event.updated_at.desc(),
            )
        ).all()

        watch_events = session.scalars(
            select(Event)
            .where(Event.homepage_section == "watch")
            .order_by(
                Event.briefing_rank.desc(),
                Event.updated_at.desc(),
            )
        ).all()

        print("=== Homepage Briefing Report ===")
        print(
            f"Critical: {len(critical_events)} "
            f"(cap {CRITICAL_CAP})"
        )

        for event in critical_events:
            print(
                f"  [{event.briefing_rank}] "
                f"#{event.id} {event.title}"
            )

        print(
            f"Watch: {len(watch_events)} "
            f"(cap {WATCH_CAP})"
        )

        for event in watch_events:
            print(
                f"  [{event.briefing_rank}] "
                f"#{event.id} {event.title}"
            )

        if len(critical_events) > CRITICAL_CAP:
            print("ERROR: Critical section exceeds cap.")

        if len(watch_events) > WATCH_CAP:
            print("ERROR: Watch section exceeds cap.")


if __name__ == "__main__":
    print_homepage_briefing_report()
