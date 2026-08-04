from app.services.openai_service import (
    generate_world_critical_decision,
)


def should_create_world_critical_event(
    article_title: str,
    article_description: str | None,
) -> dict[str, str | bool]:
    """
    Decide whether an article deserves to enter the
    World Critical event pipeline.
    """
    return generate_world_critical_decision(
        article_title=article_title,
        article_description=article_description,
    )