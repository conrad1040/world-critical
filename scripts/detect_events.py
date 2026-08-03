from app.services.event_detection_service import detect_events


def main() -> None:
    created_count = detect_events()
    print(f"Created {created_count} new events")


if __name__ == "__main__":
    main()