from database.connection import conn_context
from features.users import repo, schema
from fastapi import HTTPException
from datetime import datetime
import logging


logger = logging.getLogger(__name__)



def update_display_name(user_id: str, new_display_name: str) -> None:
    with conn_context() as conn:
        try:
            repo.update_display_name(conn, user_id, new_display_name)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to update trip")



def disable_user(user_id: str):
    with conn_context() as conn:
        try:
            current_datetime = datetime.now()
            is_deleted = True
            repo.disable_user(conn, user_id, current_datetime, is_deleted)
            repo.delete_from_trips(conn, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to disable user")

