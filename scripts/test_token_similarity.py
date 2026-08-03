from app.services.token_similarity_service import calculate_token_similarity


def main() -> None:
    title_a = "Explosion near Moscow cafe kills three - AP News"
    title_b = "At least three killed in explosion near cafe in Russia's Moscow - Al Jazeera"

    score = calculate_token_similarity(title_a, title_b)

    print(f"Token similarity: {score:.2f}")


if __name__ == "__main__":
    main()