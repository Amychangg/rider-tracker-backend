from database.connection import conn_context
from fastapi import HTTPException
from features.auth import jwt_token, repo, schema



def check_user(user_info: schema.UserLineInfo):
    with conn_context() as conn:
        try:
            user_existed =  repo.select_user(conn, user_info)
            if not user_existed:
                user_id = repo.insert_new_user_info(conn, user_info)

            access_token = jwt_token.create_access_token(user_id)
            
            return schema.LoginResponse(
                access_token = access_token
            )

        except Exception as e:
            print('error: ', e)
            raise HTTPException(status_code=500, detail="Failed to get trips")