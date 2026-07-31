from fastapi import APIRouter, status, Depends

from features.trips import services, schema
from features.auth.dependency import get_current_user



router = APIRouter(tags=["trips"], prefix="/trips")


# 取得該用戶的所有旅程及旅程有的成員
@router.get("/", response_model=list[schema.TripResponse])
def get_trips(user_id: str = Depends(get_current_user)):

    print(user_id)
    return services.get_trips_and_participated_users(user_id)


# 使用者(trip leader)創建新的旅程
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_trip(body: schema.TripCreate, user_id: str = Depends(get_current_user)):
    return services.insert_new_trips(body, user_id)


# 使用者(trip leader)更新旅程資訊
@router.put("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_trip(trip_id: str, body: schema.TripUpdate):
    services.update_trips(trip_id, body)


# 使用者(trip leader)刪除旅程
@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: str):
    services.delete_trip(trip_id)


# 使用者退出旅程
@router.delete("/{trip_id}/member/", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(trip_id: str, user_id: str = Depends(get_current_user)):
    services.delete_user_from_trip(trip_id, user_id)


# 使用者(trip leader)將其他用戶改為trip leader
@router.put("/{trip_id}/leader/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def change_leader(trip_id: str, user_id: str):
    services.update_trip_leader(trip_id, user_id)


# 撈使用者正在進行中的旅程
@router.get('/ongoing_trip/{user_id}')
def get_user_ongoing_trip(user_id: str):
    return services.get_user_ongoing_trip(user_id)


# 使用者加入旅程
@router.post('/{trip_id}/member')
def add_member(trip_id: str, user_id: str = Depends(get_current_user)):
    services.add_user_to_trip(trip_id, user_id)