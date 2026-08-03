from app.services.token_similarity_service import calculate_token_similarity

TITLE_MATCH_THRESHOLD = 0.75


def titles_match(title_a: str, title_b: str) -> bool:
    similarity = calculate_token_similarity(title_a, title_b)
    return similarity >= TITLE_MATCH_THRESHOLD