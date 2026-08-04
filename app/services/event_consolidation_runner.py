from app.database.session import SessionLocal
from app.models.event import Event
from app.services.event_consolidation_service import (
    find_consolidation_candidates,
)
from app.services.event_merge_service import (
    merge_events,
    should_merge_events,
)


def consolidate_events() -> int:
    total_merged = 0

    with SessionLocal() as session:

        while True:
            merged_this_pass = 0

            candidates = find_consolidation_candidates()

            if not candidates:
                break

            for candidate in candidates:
                event_a = session.get(
                    Event,
                    candidate["event_a_id"],
                )

                event_b = session.get(
                    Event,
                    candidate["event_b_id"],
                )

                if event_a is None or event_b is None:
                    continue

                decision = should_merge_events(
                    event_a_title=event_a.title,
                    event_a_summary=event_a.summary,
                    event_b_title=event_b.title,
                    event_b_summary=event_b.summary,
                )

                if decision["merge"] is not True:
                    continue

                if decision["confidence"] != "High":
                    continue

                keep_event = event_a
                remove_event = event_b

                if event_b.article_count > event_a.article_count:
                    keep_event = event_b
                    remove_event = event_a

                keep_event_id = keep_event.id
                remove_event_id = remove_event.id

                merge_events(
                    session=session,
                    keep_event=keep_event,
                    remove_event=remove_event,
                )

                keep_event.needs_refresh = True

                merged_this_pass += 1
                total_merged += 1

                print(
                    f"Merged event {remove_event_id} "
                    f"into event {keep_event_id}"
                )

                print(
                    f"Reason: {decision['reasoning']}"
                )

            session.commit()

            if merged_this_pass == 0:
                break

            print(
                f"Completed consolidation pass "
                f"({merged_this_pass} merges)."
            )

    return total_merged