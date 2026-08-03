from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.event import Event

IMPORTANCE_THRESHOLD = 75

CATEGORY_WEIGHTS = {
    "Conflict": 40,
    "Natural Disaster": 35,
    "Health": 30,
    "Politics": 25,
    "Economy": 20,
    "Crime": 15,
    "Technology": 10,
    "Sports": 5,
    "Entertainment": 5,
    "Other": 0,
}


def update_importance_scores() -> int:
    updated_count = 0

    with SessionLocal() as session:
        events = session.scalars(select(Event)).all()

        for event in events:
            category_score = CATEGORY_WEIGHTS.get(event.category, 0)

            score = (
                category_score
                + event.source_count * 15
                + event.article_count * 5
            )

            event.importance_score = min(score, 100)

            if event.importance_score >= IMPORTANCE_THRESHOLD:
                event.status = "Qualifying"
            else:
                event.status = "Candidate"

            updated_count += 1

        session.commit()

    return updated_count