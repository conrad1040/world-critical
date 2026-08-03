from app.models.event import Event
from app.services.openai_service import generate_contextual_match


def contextual_match(
    article_title: str,
    candidate_event: Event,
    candidate_titles: list[str],
) -> dict[str, str | bool]:
    return generate_contextual_match(
        article_title=article_title,
        event_title=candidate_event.title,
        candidate_titles=candidate_titles,
    )