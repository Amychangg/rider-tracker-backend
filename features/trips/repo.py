from database import config, utils
from features.trips import schema


def select_trips_and_participated_users(conn, user_id: str) -> list[dict]:
    sql = f"""
        SELECT
            t.trip_id,
            t.trip_title,
            t.description,
            t.leader_id,
            t.start_datetime,
            t.end_datetime,
            t.trip_type,
            t.meeting_location,
            COALESCE(
                json_agg(
                    json_build_object(
                        'user_id', u.user_id,
                        'display_name', u.display_name
                    )
                ) FILTER (WHERE tm.user_id IS NOT NULL),
                '[]'
            ) AS members
        FROM {config.TABLE_TRIPS} t
        LEFT JOIN {config.TABLE_TRIP_MEMBERS} tm ON t.trip_id = tm.trip_id
        LEFT JOIN {config.TABLE_USERS} u ON tm.user_id = u.user_id
        WHERE t.trip_id IN (
            SELECT trip_id FROM {config.TABLE_TRIP_MEMBERS} WHERE user_id = %s
        )
        GROUP BY t.trip_id
    """
    return utils.query_all(conn, sql, (user_id,))


def insert_trip(conn, trip: schema.TripCreate) -> str:
    sql = f"""
        INSERT INTO {config.TABLE_TRIPS}
            (trip_title, description, leader_id, start_datetime, end_datetime, trip_type, meeting_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    """
    result = utils.query_one(conn, sql, (
        trip.trip_title, trip.description, trip.leader_id,
        trip.start_datetime, trip.end_datetime, trip.trip_type, trip.meeting_location,
    ))
    return result["trip_id"]


def add_trip_member(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        INSERT INTO {config.TABLE_TRIP_MEMBERS} (trip_id, user_id)
        VALUES (%s, %s)
    """
    utils.execute(conn, sql, (trip_id, user_id))


def update_trip(conn, trip_id: str, trip: schema.TripUpdate) -> None:
    sql = f"""
        UPDATE {config.TABLE_TRIPS}
        SET trip_title=%s, description=%s, start_datetime=%s,
            end_datetime=%s, trip_type=%s, meeting_location=%s
        WHERE trip_id = %s
    """
    utils.execute(conn, sql, (
        trip.trip_title, trip.description, trip.start_datetime,
        trip.end_datetime, trip.trip_type, trip.meeting_location, trip_id,
    ))


def delete_trip(conn, trip_id: str) -> None:
    sql = f"""
        DELETE FROM {config.TABLE_TRIPS} 
        WHERE trip_id = %s
    """
    utils.execute(conn, sql, (trip_id,))


def delete_trip_member(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        DELETE FROM {config.TABLE_TRIP_MEMBERS} 
        WHERE trip_id = %s AND user_id = %s
    """
    utils.execute(conn, sql, (trip_id, user_id))


def update_trip_leader(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        UPDATE {config.TABLE_TRIPS} 
        SET leader_id = %s 
        WHERE trip_id = %s
    """

    utils.execute(conn, sql, (user_id, trip_id))
