from app.services.openai_service import generate_editorial_evaluation


def evaluate_event(
    headlines: list[str],
    source_count: int,
    article_count: int,
    category: str,
    importance_score: int,
) -> dict[str, str]:
    return generate_editorial_evaluation(
        headlines=headlines,
        source_count=source_count,
        article_count=article_count,
        category=category,
        importance_score=importance_score,
    )