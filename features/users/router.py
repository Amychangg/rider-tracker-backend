from fastapi import APIRouter, Depends
from features.auth.dependency import get_current_user
from features.users import services as users_services

router = APIRouter(
    tags=["users"], prefix="/users"
)

# 使用者修改名稱
@router.put('/display_name/')
def update_display_name(new_display_name: str, user_id: str = Depends(get_current_user)):
    return users_services.update_display_name(user_id, new_display_name)


# 使用者刪除帳號
@router.delete('/remove/')
def disable_user(user_id: str = Depends(get_current_user)):
    return users_services.disable_user(user_id)