from app.services.article_ingestion_service import ingest_top_headlines
from app.services.event_detection_service import detect_events
from app.services.event_metrics_service import update_event_metrics
from app.services.importance_scoring_service import update_importance_scores
from app.services.event_category_update_service import update_event_categories

def main() -> None:
    print("=== World Critical Update ===")

    articles_created = ingest_top_headlines(page_size=10)
    print(f"Articles added: {articles_created}")

    events_created = detect_events()
    print(f"Events created: {events_created}")

    categories_updated = update_event_categories()
    print(f"Event categories updated: {categories_updated}")

    events_updated = update_event_metrics()
    print(f"Event metrics updated: {events_updated}")

    scores_updated = update_importance_scores()
    print(f"Importance scores updated: {scores_updated}")

    print("Update complete.")

if __name__ == "__main__":
    main()