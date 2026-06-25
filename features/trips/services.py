from database import connection
from features.trips import repo
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


def get_all_trips():
    conn = None

    try:
        conn = connection.get_conn()
        result =  repo.select_all_trips(conn)
        print(result)

        return result
    
    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail="Failed to get trips"
        )
    
    finally:
        if conn:
            connection.release_conn(conn)