from fastapi import APIRouter, HTTPException, Query

from app.schemas.event import EventResponse
from app.services.event_detail_service import get_event
from app.services.event_search_service import search_events
from app.services.events_service import get_events

router = APIRouter()


@router.get("/events")
def read_events():
    return get_events()


@router.get("/events/search")
def read_event_search(
    q: str = Query(default=""),
):
    return search_events(q)


@router.get(
    "/events/{event_id}",
    response_model=EventResponse,
)
def read_event(event_id: int):
    event = get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event