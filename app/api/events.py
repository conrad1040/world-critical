from fastapi import APIRouter

from app.services.events_service import get_events

router = APIRouter()


@router.get("/events")
def events():
    return {"events": get_events()}