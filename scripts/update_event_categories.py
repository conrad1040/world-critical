from app.services.event_category_update_service import update_event_categories


def main() -> None:
    updated_count = update_event_categories()
    print(f"Updated categories for {updated_count} events")


if __name__ == "__main__":
    main()