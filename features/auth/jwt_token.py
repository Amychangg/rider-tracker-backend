from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(user_id: str) -> str:
    """
    建立 JWT Access Token
    """

    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": user_id,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    驗證 JWT 並解碼回傳 payload
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無效或已過期的 Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解碼 Token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        # 包含 Token 過期 (ExpiredSignatureError) 或 簽名錯誤 (DecodeError)
        raise credentials_exception