from collections import defaultdict

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.article import Article
from app.models.event import Event
from app.services.contextual_matching_service import contextual_match
from app.services.event_matching_service import titles_match
from app.services.event_text_service import (
    create_event_summary,
    create_event_title,
)
from app.services.title_similarity_service import (
    calculate_title_similarity,
)
from app.services.token_similarity_service import (
    calculate_token_similarity,
)

CONTEXTUAL_MATCH_THRESHOLD = 0.35
MAX_CONTEXTUAL_CANDIDATES = 3


def _candidate_similarity(
    article_title: str,
    event_title: str,
) -> float:
    token_similarity = calculate_token_similarity(
        article_title,
        event_title,
    )

    title_similarity = calculate_title_similarity(
        article_title,
        event_title,
    )

    return max(token_similarity, title_similarity)


def detect_events() -> int:
    created_count = 0

    with SessionLocal() as session:
        unassigned_articles = session.scalars(
            select(Article)
            .where(Article.event_id.is_(None))
            .order_by(Article.published_at)
        ).all()

        events = session.scalars(
            select(Event)
        ).all()

        assigned_articles = session.scalars(
            select(Article).where(
                Article.event_id.is_not(None)
            )
        ).all()

        event_article_titles: dict[int, list[str]] = defaultdict(list)

        for assigned_article in assigned_articles:
            if assigned_article.event_id is not None:
                event_article_titles[
                    assigned_article.event_id
                ].append(assigned_article.title)

        for article in unassigned_articles:
            matched_event: Event | None = None

            # First, use the fast deterministic matcher.
            for event in events:
                if titles_match(article.title, event.title):
                    matched_event = event

                    print(
                        f"Deterministic match: article "
                        f"'{article.title}' -> event {event.id}"
                    )

                    break

            # If there is no strong deterministic match, build a
            # shortlist for contextual evaluation.
            if matched_event is None:
                possible_matches: list[tuple[float, Event]] = []

                for event in events:
                    similarity = _candidate_similarity(
                        article.title,
                        event.title,
                    )

                    if similarity >= CONTEXTUAL_MATCH_THRESHOLD:
                        possible_matches.append(
                            (similarity, event)
                        )

                possible_matches.sort(
                    key=lambda item: item[0],
                    reverse=True,
                )

                possible_matches = possible_matches[
                    :MAX_CONTEXTUAL_CANDIDATES
                ]

                confidence_rank = {
                    "High": 3,
                    "Medium": 2,
                    "Low": 1,
                }

                best_match = None

                for similarity, candidate_event in possible_matches:
                    candidate_titles = event_article_titles.get(
                        candidate_event.id,
                        [],
                    )

                    decision = contextual_match(
                        article_title=article.title,
                        candidate_event=candidate_event,
                        candidate_titles=candidate_titles,
                    )

                    if decision.get("match") is not True:
                        continue

                    confidence = str(
                        decision.get("confidence", "Low")
                    )

                    candidate_score = (
                        confidence_rank.get(confidence, 0),
                        similarity,
                    )

                    if (
                        best_match is None
                        or candidate_score > best_match["score"]
                    ):
                        best_match = {
                            "event": candidate_event,
                            "score": candidate_score,
                            "similarity": similarity,
                            "decision": decision,
                        }

                if best_match is not None:
                    matched_event = best_match["event"]
                    decision = best_match["decision"]

                    print(
                        f"Contextual match: article "
                        f"'{article.title}' -> event "
                        f"{matched_event.id} "
                        f"(similarity={best_match['similarity']:.2f}, "
                        f"confidence={decision['confidence']})"
                    )

                    print(
                        "Reason: "
                        f"{decision.get('reasoning', '')}"
                    )

            # If neither matching method found an event,
            # create a new one.
            if matched_event is None:
                matched_event = Event(
                    title=create_event_title(article.title),
                    summary=create_event_summary(article.title),
                    importance_score=0,
                    status="Candidate",
                    needs_refresh=True,
                )

                session.add(matched_event)
                session.flush()

                events.append(matched_event)
                created_count += 1

                print(
                    f"Created event {matched_event.id}: "
                    f"{matched_event.title}"
                )

            article.event_id = matched_event.id
            matched_event.needs_refresh = True

            # Keep the in-memory article-title map current so later
            # articles in this same run can use newly attached coverage.
            event_article_titles[matched_event.id].append(
                article.title
            )

        session.commit()

    return created_count