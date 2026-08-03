from app.services.title_normalization_service import normalize_title


def get_title_tokens(title: str) -> set[str]:
    return set(normalize_title(title).split())


def calculate_token_similarity(
    title_a: str,
    title_b: str,
) -> float:
    """
    Dice similarity balances shared words against the total
    size of both titles.

    1.0 means identical token sets.
    0.0 means no shared tokens.
    """
    tokens_a = get_title_tokens(title_a)
    tokens_b = get_title_tokens(title_b)

    if not tokens_a or not tokens_b:
        return 0.0

    shared_count = len(tokens_a & tokens_b)

    return (2 * shared_count) / (
        len(tokens_a) + len(tokens_b)
    )


def calculate_token_containment(
    title_a: str,
    title_b: str,
) -> float:
    """
    Measures how much of the shorter title is contained in
    the longer title.
    """
    tokens_a = get_title_tokens(title_a)
    tokens_b = get_title_tokens(title_b)

    if not tokens_a or not tokens_b:
        return 0.0

    shared_count = len(tokens_a & tokens_b)
    smaller_size = min(len(tokens_a), len(tokens_b))

    return shared_count / smaller_size


def calculate_jaccard_similarity(
    title_a: str,
    title_b: str,
) -> float:
    tokens_a = get_title_tokens(title_a)
    tokens_b = get_title_tokens(title_b)

    if not tokens_a or not tokens_b:
        return 0.0

    shared_count = len(tokens_a & tokens_b)
    total_unique_tokens = len(tokens_a | tokens_b)

    return shared_count / total_unique_tokens