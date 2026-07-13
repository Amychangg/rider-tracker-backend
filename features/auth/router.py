from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
import httpx
from core.config import settings
from features.auth import services, schema



router = APIRouter(
    tags=["auth"], prefix="/auth"
)



# 接收flutter回傳的line auth code
from fastapi import HTTPException
import httpx

@router.post('/line/login')
async def line_login_callback(payload: dict):
    print('1111 接收到的 Payload:', payload)
    
    # 1. 直接從前端傳過來的 payload 裡面取出 code
    code = payload.get("access_token")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in payload")
        
    # 2. 直接拿這個 token 去 LINE 的 /v2/profile API 抓取使用者資料
    async with httpx.AsyncClient() as client:
        profile_response = await client.get(
            "https://api.line.me/v2/profile",
            headers={"Authorization": f"Bearer {code}"} # 💡 這裡一定要加 Bearer
        )
        
        # 如果 LINE 回報錯誤（例如 token 過期或假的），這裡會直接抓到
        if profile_response.status_code != 200:
            print("LINE 驗證失敗:", profile_response.text)
            raise HTTPException(status_code=401, detail="Invalid or expired LINE token")
            
        line_profile = profile_response.json()
        
    # 3. 成功拿到 LINE 的不重複使用者 ID 與暱稱
    user_info = schema.UserLineInfo(
        line_user_id = line_profile.get("userId"),  # 這是 LINE 獨一無二的識別碼
        display_name = line_profile.get("displayName"),
        picture_url = line_profile.get("pictureUrl") # 大頭貼網址（選用）
    )

    print('✨ 成功串接 LINE 用戶！', user_info)
    
    return services.check_user(user_info)
