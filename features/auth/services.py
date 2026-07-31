from database.connection import conn_context
from fastapi import HTTPException
from features.auth import jwt_token, repo, schema



def check_user(user_info: schema.UserLineInfo):
    with conn_context() as conn:
        try:
            user_existed = repo.select_user(conn, user_info)
            if user_existed:
                # 建議：如果舊用戶有資料更新，可以順便 Update DB 中的 display_name / picture
                user_data = user_existed[0]
            else:
                user_data = repo.insert_new_user_info(conn, user_info)

            user_id = user_data["user_id"]
            access_token = jwt_token.create_access_token(user_id)
            
            return schema.LoginResponse(
                access_token = access_token,
                user = user_info
            )

        except Exception as e:
            print('error: ', e)
            raise HTTPException(status_code=500, detail="Failed to get trips")