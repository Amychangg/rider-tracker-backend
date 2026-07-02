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


def insert_new_trips(trip: schema.TripCreate) -> str:
    with conn_context() as conn:
        try:
            conn.autocommit = False
            trip_id = repo.insert_trip(conn, trip)
            repo.add_trip_member(conn, trip_id, trip.leader_id)
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
