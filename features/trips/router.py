from fastapi import APIRouter
from features.trips import services
from features.trips import schema

import mock_data

router = APIRouter(
    tags=["trips"], prefix="/trips"
)




# 取得旅程
@router.get('/get_trips/{user_id}')
def get_trips(user_id: str):
    print(user_id)

    # user_participated_trips = services.get_user_participated_trips(user_id)
    user_participated_trips = mock_data.EXISTED_TRIP
    all_users = mock_data.EXISTED_USER
    print(user_participated_trips)

    return user_participated_trips


# 創建旅程
@router.post('/new_trip/')
def new_trip(trip: schema.Trip):
    print(trip)
    


# 更新旅程
@router.put('/update_trip/')
def update_trip():
    pass


# 刪除旅程
@router.delete('/delete_trip/')
def delete_trip():
    pass