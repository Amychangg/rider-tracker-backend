from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings




def create_access_token(user_id: str) -> str:
    """
    建立 JWT Access Token
    """

    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": user_id,
        "exp": expire,
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