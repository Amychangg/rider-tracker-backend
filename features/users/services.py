from database.connection import conn_context
from features.users import repo, schema
from fastapi import HTTPException

import logging


logger = logging.getLogger(__name__)



def update_display_name(user_id: str, new_display_name: str) -> None:
    with conn_context() as conn:
        try:
            repo.update_display_name(conn, user_id, new_display_name)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to update trip")
