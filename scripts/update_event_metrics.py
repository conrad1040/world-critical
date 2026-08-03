from app.services.event_metrics_service import update_event_metrics


def main() -> None:
    updated_count = update_event_metrics()
    print(f"Updated metrics for {updated_count} events")


if __name__ == "__main__":
    main()