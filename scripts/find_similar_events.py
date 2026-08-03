from itertools import combinations

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event
from app.services.token_similarity_service import (
    calculate_token_similarity,
)
from app.services.title_similarity_service import (
    calculate_title_similarity,
)


def main() -> None:
    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

    print(f"Loaded {len(events)} events\n")

    similar_pairs = []

    for event_a, event_b in combinations(events, 2):
        token_score = calculate_token_similarity(
            event_a.title,
            event_b.title,
        )

        title_score = calculate_title_similarity(
            event_a.title,
            event_b.title,
        )

        score = max(token_score, title_score)

        if score >= 0.45:
            similar_pairs.append(
                (
                    score,
                    event_a,
                    event_b,
                    token_score,
                    title_score,
                )
            )

    similar_pairs.sort(
        key=lambda pair: pair[0],
        reverse=True,
    )

    for score, a, b, token, title in similar_pairs:
        print("-" * 80)
        print(f"Score: {score:.2f}")
        print(f"Token: {token:.2f}")
        print(f"Title: {title:.2f}")
        print()
        print(f"{a.id}: {a.title}")
        print(f"{b.id}: {b.title}")
        print()

    print(f"Found {len(similar_pairs)} possible duplicates.")
    

if __name__ == "__main__":
    main()