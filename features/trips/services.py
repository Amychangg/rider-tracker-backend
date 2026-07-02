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
        conn.autocommit = False   # 👈 關鍵

        # 先insert到trips中，並回傳trip_id
        trip_id = repo.insert_new_trips(conn, trip)
        # 再將創建者個user_id and trip_id insert到trip_members
        repo.add_user_to_trip(conn, trip_id, trip.leader_id)

        conn.commit()            # 👈 成功才提交

        return trip_id

    except Exception as e:
        if conn:
            conn.rollback()      # 👈 失敗回滾

        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to create trip"
        )

    finally:
        if conn:
            connection.release_conn(conn)





def delete_trip(trip_id: str):
    conn = None
    try:
        conn = connection.get_conn()
        repo.delete_trip(conn, trip_id)

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete trip"
        )

    finally:
        if conn:
            connection.release_conn(conn)    




def update_trips(trip: schema.Trip, trip_id: str):
    conn = None
    try:
        conn = connection.get_conn()
        repo.update_trip(conn, trip, trip_id)

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete trip"
        )

    finally:
        if conn:
            connection.release_conn(conn)  




def delete_user_from_trip(trip_id: str, user_id: str):
    conn = None
    try:
        conn = connection.get_conn()
        repo.delete_user_from_trip(conn, trip_id, user_id)

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete trip"
        )

    finally:
        if conn:
            connection.release_conn(conn)    



def update_trip_leader(trip_id, user_id):
    conn = None
    try:
        conn = connection.get_conn()
        repo.update_trip_leader(conn, trip_id, user_id)

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to delete trip"
        )

    finally:
        if conn:
            connection.release_conn(conn)    
