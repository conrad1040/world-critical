from app.services.openai_service import (
    generate_event_update,
)


def evaluate_event(
    current_summary: str | None,
    current_latest_development: str | None,
    current_why_it_matters: str | None,
    current_what_happens_next: str | None,
    new_articles: list[dict[str, str]],
    source_count: int,
    article_count: int,
    category: str,
    importance_score: int,
) -> dict[str, str]:
    return generate_event_update(
        current_summary=current_summary,
        current_latest_development=current_latest_development,
        current_why_it_matters=current_why_it_matters,
        current_what_happens_next=current_what_happens_next,
        new_articles=new_articles,
        source_count=source_count,
        article_count=article_count,
        category=category,
        importance_score=importance_score,
    )