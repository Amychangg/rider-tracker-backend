from fastapi import APIRouter
from features.trips import services
from features.trips import schema
from core.config import HOST

import mock_data

router = APIRouter(
    tags=["trips"], prefix="/trips"
)




# 取得旅程
@router.get('/get_trips/{user_id}')
def get_trips(user_id: str):

    if HOST =='172.16.16.77':
        user_participated_trips = services.get_trips_and_participated_users(user_id)
        print(user_participated_trips)
    else:
        user_participated_trips = mock_data.EXISTED_TRIP
    
    return user_participated_trips


# 創建旅程
@router.post('/new_trip/')
def new_trip(trip: schema.Trip):
    print(trip)
    
    services.insert_new_trips(trip)


# 更新旅程
@router.put('/update_trip/')
def update_trip():
    pass


# 刪除旅程
@router.delete('/delete_trip/')
def delete_trip():
    pass