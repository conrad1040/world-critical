from app.services.openai_service import generate_event_text


def main():
    title, summary = generate_event_text(
        [
            "At least three killed in explosion near cafe in Russia's Moscow",
            "Several people killed in Moscow restaurant blast, officials say",
        ]
    )

    print("TITLE:")
    print(title)

    print("\nSUMMARY:")
    print(summary)


if __name__ == "__main__":
    main()