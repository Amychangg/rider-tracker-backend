from database import utils
from core.config import settings
from features.auth import schema


def select_user(conn, user_info: schema.UserLineInfo):
    sql = f"""
        select user_id, display_name, avatar_url from { settings.TABLE_USERS }
        where line_id=%s
    """
    return utils.query_all(conn, sql, (user_info.line_user_id,))




def insert_new_user_info(conn, user_info: schema.UserLineInfo):
    sql = f"""
    INSERT INTO { settings.TABLE_USERS } (line_id, display_name) 
    VALUES (%s, %s)
    RETURNING user_id
    """

    return utils.query_one(conn, sql, (user_info.line_user_id, user_info.display_name))
