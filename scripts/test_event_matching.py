from app.services.event_matching_service import titles_match


def main() -> None:
    related_a = "Explosion near Moscow cafe kills three - AP News"
    related_b = (
        "At least three killed in explosion near cafe in Russia's Moscow "
        "- Al Jazeera"
    )
    unrelated = "Federal Reserve announces new interest rate decision"

    print("Related:", titles_match(related_a, related_b))
    print("Unrelated:", titles_match(related_a, unrelated))


if __name__ == "__main__":
    main()