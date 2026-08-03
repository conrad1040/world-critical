from app.services.title_similarity_service import calculate_title_similarity


def main() -> None:
    title_a = "Explosion near Moscow cafe kills three - AP News"
    title_b = "At least three killed in explosion near cafe in Russia's Moscow - Al Jazeera"

    score = calculate_title_similarity(title_a, title_b)

    print(f"Similarity: {score:.2f}")


if __name__ == "__main__":
    main()