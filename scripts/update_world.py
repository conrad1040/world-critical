from app.services.article_ingestion_service import ingest_top_headlines
from app.services.event_detection_service import detect_events


def main() -> None:
    print("=== World Critical Update ===")

    articles_created = ingest_top_headlines(page_size=10)
    print(f"Articles added: {articles_created}")

    events_created = detect_events()
    print(f"Events created: {events_created}")

    print("Update complete.")


if __name__ == "__main__":
    main()