from database import utils
from core.config import settings
from features.users import schema



def update_display_name(conn, user: schema.User):
    sql = f"""
        UPDATE {settings.TABLE_USERS}
        SET 
            display_name=%s
        WHERE user_id = %s
    """
    utils.execute(conn, sql, (
        user.display_name, user.user_id
    ))




def disable_user(conn, user_id: str, current_datetime, is_deleted: bool):
    sql = f"""
        UPDATE {settings.TABLE_USERS}
        SET 
            is_deleted=%s,
            deleted_at=%s
        WHERE user_id = %s
    """
    utils.execute(conn, sql, (
        is_deleted, current_datetime, user_id
    ))




def delete_from_trips(conn, user_id: str):
    sql = f"""
        DELETE FROM {settings.TABLE_TRIP_MEMBERS}
        WHERE user_id = %s
    """
    utils.execute(conn, sql, (
        user_id
    ))