from database.connection import conn_context
from features.trips import repo, schema
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


def get_trips_and_participated_users(user_id: str) -> list[dict]:
    with conn_context() as conn:
        try:
            return repo.select_trips_and_participated_users(conn, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to get trips")


def insert_new_trips(trip: schema.TripCreate, user_id: str) -> str:
    with conn_context() as conn:
        try:
            conn.autocommit = False
            trip_id = repo.insert_trip(conn, trip, user_id)
            repo.add_trip_member(conn, trip_id, user_id)
            conn.commit()
            return trip_id
        except Exception as e:
            if conn:
                conn.rollback()
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to create trip")


def update_trips(trip_id: str, trip: schema.TripUpdate) -> None:
    with conn_context() as conn:
        try:
            repo.update_trip(conn, trip_id, trip)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to update trip")


def delete_trip(trip_id: str) -> None:
    with conn_context() as conn:
        try:
            repo.delete_trip(conn, trip_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to delete trip")


def delete_user_from_trip(trip_id: str, user_id: str) -> None:
    with conn_context() as conn:
        try:
            repo.delete_trip_member(conn, trip_id, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to remove member from trip")


def update_trip_leader(trip_id: str, user_id: str) -> None:
    with conn_context() as conn:
        try:
            repo.update_trip_leader(conn, trip_id, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to update trip leader")



def get_user_ongoing_trip(user_id: str) -> list[dict]:
    with conn_context() as conn:
        try:
            return repo.get_user_ongoing_trip(conn, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to get trips")
        

def add_user_to_trip(joining_trip_id: str, user_id: str):
    with conn_context() as conn:
        try:
            user_trips = repo.select_user_all_trips(conn, user_id)
            joining_trip = repo.select_trip(joining_trip_id)
            check_time_availability(user_trips, joining_trip)

            return repo.add_trip_member(conn, joining_trip_id, user_id)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail="Failed to get trips")




# 檢查使用者現在要加入的旅程的起迄時間是否與現有旅程的起迄時間衝突
def check_time_availability(user_trips, joining_trip):
    pass