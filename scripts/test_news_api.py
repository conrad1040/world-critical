from app.services.news_service import fetch_top_headlines


def main() -> None:
    articles = fetch_top_headlines(page_size=5)

    for article in articles:
        print(article["title"])


if __name__ == "__main__":
    main()