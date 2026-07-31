from fastapi import APIRouter, Depends
from features.auth.dependency import get_current_user
from features.users import services as users_services

router = APIRouter(
    tags=["users"], prefix="/users"
)


@router.put('/display_name/')
def update_display_name(user_id: str = Depends(get_current_user)):
    print(user_id)

    users_services.update_display_name()