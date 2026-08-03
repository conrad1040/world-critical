from app.services.editor_service import evaluate_event


def main() -> None:
    print("Running editorial evaluation...")

    result = evaluate_event(
        headlines=[
            "At least three killed in explosion near cafe in Russia's Moscow",
            "Several people killed in Moscow restaurant blast, officials say",
        ],
        source_count=2,
        article_count=2,
        category="Conflict",
        importance_score=80,
    )

    print()

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()