from fastapi import APIRouter, HTTPException

from app.services.event_detail_service import get_event
from app.services.events_service import get_events

router = APIRouter()


@router.get("/events")
def read_events():
    return {"events": get_events()}


@router.get("/events/{event_id}")
def read_event(event_id: int):
    event = get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event