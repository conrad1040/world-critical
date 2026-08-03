import re

from app.services.title_normalization_service import normalize_title
from app.services.title_similarity_service import (
    calculate_title_similarity,
)
from app.services.token_similarity_service import (
    calculate_jaccard_similarity,
    calculate_token_containment,
    calculate_token_similarity,
    get_title_tokens,
)

HYBRID_MATCH_THRESHOLD = 0.62
STRONG_CONTAINMENT_THRESHOLD = 0.75


def _extract_years(title: str) -> set[str]:
    return set(re.findall(r"\b(?:19|20)\d{2}\b", title))


def _has_conflicting_years(
    title_a: str,
    title_b: str,
) -> bool:
    years_a = _extract_years(title_a)
    years_b = _extract_years(title_b)

    return bool(
        years_a
        and years_b
        and years_a.isdisjoint(years_b)
    )


def titles_match(title_a: str, title_b: str) -> bool:
    normalized_a = normalize_title(title_a)
    normalized_b = normalize_title(title_b)

    if not normalized_a or not normalized_b:
        return False

    if normalized_a == normalized_b:
        return True

    if _has_conflicting_years(title_a, title_b):
        return False

    tokens_a = get_title_tokens(title_a)
    tokens_b = get_title_tokens(title_b)
    shared_tokens = tokens_a & tokens_b
    shared_count = len(shared_tokens)

    # Avoid matching headlines based on one generic shared word.
    if shared_count < 2:
        return False

    dice_similarity = calculate_token_similarity(
        title_a,
        title_b,
    )
    containment = calculate_token_containment(
        title_a,
        title_b,
    )
    jaccard = calculate_jaccard_similarity(
        title_a,
        title_b,
    )
    title_similarity = calculate_title_similarity(
        title_a,
        title_b,
    )

    # A strong containment match is reliable when at least
    # three meaningful words overlap.
    if (
        containment >= STRONG_CONTAINMENT_THRESHOLD
        and shared_count >= 3
    ):
        return True

    hybrid_score = (
        0.35 * containment
        + 0.30 * dice_similarity
        + 0.20 * jaccard
        + 0.15 * title_similarity
    )

    return hybrid_score >= HYBRID_MATCH_THRESHOLD