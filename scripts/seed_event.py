from app.database.session import SessionLocal
from app.models.event import Event


def main() -> None:
    with SessionLocal() as session:
        event = Event(
            title="World Critical Backend Started",
            summary="The initial World Critical backend and database are operational.",
            importance_score=100,
            status="Development",
        )

        session.add(event)
        session.commit()

        print(f"Created event with ID {event.id}")


if __name__ == "__main__":
    main()