from itertools import combinations

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.title_similarity_service import (
    calculate_title_similarity,
)
from app.services.token_similarity_service import (
    calculate_token_similarity,
)

CONSOLIDATION_CANDIDATE_THRESHOLD = 0.55


def _event_similarity(
    event_a: Event,
    event_b: Event,
) -> float:
    token_similarity = calculate_token_similarity(
        event_a.title,
        event_b.title,
    )

    title_similarity = calculate_title_similarity(
        event_a.title,
        event_b.title,
    )

    return max(
        token_similarity,
        title_similarity,
    )


def find_consolidation_candidates() -> list[dict]:
    with SessionLocal() as session:
        events = session.scalars(
            select(Event).order_by(Event.updated_at.desc())
        ).all()

        candidates: list[dict] = []

        for event_a, event_b in combinations(events, 2):
            similarity = _event_similarity(
                event_a,
                event_b,
            )

            if similarity < CONSOLIDATION_CANDIDATE_THRESHOLD:
                continue

            candidates.append(
                {
                    "event_a_id": event_a.id,
                    "event_a_title": event_a.title,
                    "event_a_summary": event_a.summary,
                    "event_b_id": event_b.id,
                    "event_b_title": event_b.title,
                    "event_b_summary": event_b.summary,
                    "similarity": similarity,
                }
            )

        candidates.sort(
            key=lambda candidate: candidate["similarity"],
            reverse=True,
        )

        return candidates