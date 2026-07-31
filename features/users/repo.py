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