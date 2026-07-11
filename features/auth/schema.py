from pydantic import BaseModel


class UserLineInfo(BaseModel):
    line_user_id: str
    display_name: str
    picture_url: str


class JwtRequiredInfo(BaseModel):
    user_id: str
    display_name: str
    avatar_path: str