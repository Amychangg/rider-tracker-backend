from fastapi import APIRouter
from features.trips import services
from features.trips import schema

router = APIRouter(
    tags=["trips"], prefix="/trips"
)




# 取得旅程
@router.get('/get_trips/')
def get_trips():
    return services.get_all_trips()


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