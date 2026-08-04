from app.services.article_ingestion_service import ingest_top_headlines
from app.services.event_category_update_service import update_event_categories
from app.services.event_detection_service import detect_events
from app.services.event_metrics_service import update_event_metrics
from app.services.event_refresh_service import refresh_event_text
from app.services.homepage_curation_service import curate_homepage
from app.services.importance_scoring_service import update_importance_scores
from app.services.event_consolidation_runner import (
    consolidate_events,
)

def main() -> None:
    print("=== World Critical Update ===")

    articles_created = ingest_top_headlines(page_size=10)

    if articles_created == 0:
        print("No new articles ingested.")
    else:
        print(f"Articles added: {articles_created}")

    events_created = detect_events()
    print(f"Events created: {events_created}")

    events_merged = consolidate_events()
    print(f"Events merged: {events_merged}")

    categories_updated = update_event_categories()
    print(f"Event categories updated: {categories_updated}")

    metrics_updated = update_event_metrics()
    print(f"Event metrics updated: {metrics_updated}")

    scores_updated = update_importance_scores()
    print(f"Importance scores updated: {scores_updated}")

    text_updated = refresh_event_text()
    print(f"Event text updated: {text_updated}")

    briefing = curate_homepage()
    print(
        "Homepage briefing curated: "
        f"{briefing['critical_count']} critical, "
        f"{briefing['watch_count']} watch "
        f"({briefing['mode']})"
    )

    print("Update complete.")


if __name__ == "__main__":
    main()
