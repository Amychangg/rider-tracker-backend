from pydantic import BaseModel


class UserLineInfo(BaseModel):
    line_user_id: str
    display_name: str
    picture_url: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: UserLineInfo