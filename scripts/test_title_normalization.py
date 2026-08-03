from app.services.title_normalization_service import normalize_title


def main() -> None:
    title = "At least three killed in explosion near cafe in Russia’s Moscow - Al Jazeera"
    print(normalize_title(title))


if __name__ == "__main__":
    main()