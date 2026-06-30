from database import connection
from features.trips import repo, schema
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


# def get_all_trips():
#     conn = None

#     try:
#         conn = connection.get_conn()
#         result =  repo.select_all_trips(conn)

#         return result
    
#     except Exception as e:

#         logger.exception(e)

#         raise HTTPException(
#             status_code=500,
#             detail="Failed to get trips"
#         )
    
#     finally:
#         if conn:
#             connection.release_conn(conn)




def get_trips_and_participated_users(user_id: str):
    conn = None

    try:
        conn = connection.get_conn()
        result =  repo.select_trips_and_participated_users(conn, user_id)

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



def insert_new_trips(trip: schema.Trip):
    conn = None

    try:
        conn = connection.get_conn()
        result =  repo.insert_new_trips(conn, trip)

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