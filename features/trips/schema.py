from pydantic import BaseModel
from datetime import datetime




class Trip(BaseModel):
    trip_title: str
    description: str
    leader_id: str
    start_datetime: datetime
    end_datetime: datetime
    trip_type: str
    meeting_location: str
