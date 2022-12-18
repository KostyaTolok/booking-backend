from typing import List

from fastapi import APIRouter, status

from app.schemas import LogEvent
from app.services import EventService

router = APIRouter(tags=["IoT Logs"])


@router.get(
    "/",
    response_model=List[LogEvent],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Problems with AWS or other stuff"
        },
    },
)
def get_door_event_logs():
    log_events = EventService().get_all_logs()
    return log_events


@router.get(
    "/{apartment_id}/",
    response_model=List[LogEvent],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Problems with AWS or other stuff"
        },
    },
)
def get_door_event_logs_by_apartment_id(apartment_id: int):
    log_events = EventService().get_logs_by_apartment_id(apartment_id)
    return log_events
