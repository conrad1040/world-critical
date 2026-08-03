from app.services.event_categorization_service import categorize_event


def main() -> None:
    titles = [
        "Earthquake strikes coastal Japan",
        "Missile strike reported near capital",
        "Federal Reserve announces interest rate decision",
        "Pixel 11 specifications leaked",
        "WWE SummerSlam results",
    ]

    for title in titles:
        print(f"{categorize_event(title)}: {title}")


if __name__ == "__main__":
    main()