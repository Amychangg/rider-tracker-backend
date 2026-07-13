from pydantic import BaseModel
from datetime import datetime


class TripCreate(BaseModel):
    trip_title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    trip_type: str
    meeting_location: str


class TripUpdate(BaseModel):
    trip_title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    trip_type: str
    meeting_location: str


class TripResponse(BaseModel):
    trip_id: str
    trip_title: str
    description: str
    leader_id: str
    start_datetime: datetime
    end_datetime: datetime
    trip_type: str
    meeting_location: str
    members: list[dict] = []
