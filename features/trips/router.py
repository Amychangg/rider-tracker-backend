from fastapi import APIRouter
from features.trips import services
from features.trips import schema
from core.config import HOST

import mock_data

router = APIRouter(
    tags=["trips"], prefix="/trips"
)



# 取得旅程
@router.get('/{user_id}/a')
def get_trips(user_id: str):

    if HOST =='172.16.16.77':
        user_participated_trips = services.get_trips_and_participated_users(user_id)
        # print(user_participated_trips)
    else:
        user_participated_trips = mock_data.EXISTED_TRIP
    
    return user_participated_trips


# 創建旅程
@router.post('/')
def new_trip(trip: schema.Trip):    
    return services.insert_new_trips(trip)



# 更新旅程
@router.put('/{trip_id}')
def update_trip(trip: schema.Trip, trip_id: str):
    return services.update_trips(trip, trip_id)


# 刪除旅程
@router.delete('/{trip_id}')
def delete_trip(trip_id: str):

    return services.delete_trip(trip_id)
    



@router.delete('/{trip_id}/member/{user_id}')
def delete_user_from_trip(trip_id: str, user_id: str):
    return services.delete_user_from_trip(trip_id, user_id)



@router.put('/{trip_id}/leader/{user_id}')
def update_trip_leader(trip_id: str, user_id: str):
    print(trip_id, user_id)

    return services.update_trip_leader(trip_id, user_id)
