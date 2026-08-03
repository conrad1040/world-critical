from app.services.title_normalization_service import normalize_title


def calculate_token_similarity(title_a: str, title_b: str) -> float:
    tokens_a = set(normalize_title(title_a).split())
    tokens_b = set(normalize_title(title_b).split())

    if not tokens_a or not tokens_b:
        return 0.0

    shared_tokens = len(tokens_a & tokens_b)
    smaller_title_size = min(len(tokens_a), len(tokens_b))

    return shared_tokens / smaller_title_size