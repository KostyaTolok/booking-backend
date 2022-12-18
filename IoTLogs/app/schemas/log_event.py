from pydantic import BaseModel


class LogEvent(BaseModel):
    apartment_id: int
    source: str
    timestamp: int
