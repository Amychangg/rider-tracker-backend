from fastapi import APIRouter, status

from features.trips import services
from features.trips.schema import TripCreate, TripUpdate, TripResponse

router = APIRouter(tags=["trips"], prefix="/trips")


@router.get("/{user_id}", response_model=list[TripResponse])
def get_trips(user_id: str):
    return services.get_trips_and_participated_users(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_trip(body: TripCreate):
    return services.insert_new_trips(body)


@router.put("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_trip(trip_id: str, body: TripUpdate):
    services.update_trips(trip_id, body)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: str):
    services.delete_trip(trip_id)


@router.delete("/{trip_id}/member/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(trip_id: str, user_id: str):
    services.delete_user_from_trip(trip_id, user_id)


@router.put("/{trip_id}/leader/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def change_leader(trip_id: str, user_id: str):
    services.update_trip_leader(trip_id, user_id)



@router.get('/ongoing_trip/{user_id}')
def get_user_ongoing_trip(user_id: str):
    return services.get_user_ongoing_trip(user_id)
