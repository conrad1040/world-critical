from difflib import SequenceMatcher

from app.services.title_normalization_service import normalize_title


def calculate_title_similarity(
    title_a: str,
    title_b: str,
) -> float:
    normalized_a = normalize_title(title_a)
    normalized_b = normalize_title(title_b)

    if not normalized_a or not normalized_b:
        return 0.0

    return SequenceMatcher(
        None,
        normalized_a,
        normalized_b,
    ).ratio()