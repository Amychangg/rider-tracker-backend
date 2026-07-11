from datetime import datetime, timedelta, timezone
import jwt as jwt
from core.config import settings
from features.auth import schema



def create_access_token(jwt_info: schema.JwtRequiredInfo) -> str:
    """
    建立 JWT Access Token
    """

    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": jwt_info.user_id,
        "exp": expire,
        "name": jwt_info.display_name,
        "avatar": jwt_info.avatar_path
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    """
    驗證 JWT 並回傳 payload
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    return payload