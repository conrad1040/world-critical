from app.services.article_ingestion_service import ingest_top_headlines


def main() -> None:
    created_count = ingest_top_headlines(page_size=5)
    print(f"Created {created_count} new articles")


if __name__ == "__main__":
    main()