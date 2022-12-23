from typing import Any, Dict, Optional

from fastapi import APIRouter, Response

from src.db.models.event import Event
from src.api.db.event import get_event
from src.utils.decorators import async_fail_gracefully

router = APIRouter()


@router.get("/")
async def read_root():
    return {"name": "Match Router"}


@router.get("/{event_id}")
@async_fail_gracefully
async def read_event(response: Response, event_id: str) -> Dict[str, Any]:
    event: Optional[Event] = await get_event(event_id)

    if event is None:
        raise Exception("Event not found")

    event_name = event.name

    out = {
        "event_name": event_name,
    }

    return out
