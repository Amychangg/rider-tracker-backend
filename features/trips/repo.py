from database import utils
from core.config import settings
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
        FROM {settings.TABLE_TRIPS} t
        LEFT JOIN {settings.TABLE_TRIP_MEMBERS} tm ON t.trip_id = tm.trip_id
        LEFT JOIN {settings.TABLE_USERS} u ON tm.user_id = u.user_id
        WHERE t.trip_id IN (
            SELECT trip_id FROM {settings.TABLE_TRIP_MEMBERS} WHERE user_id = %s
        )
        GROUP BY t.trip_id
    """
    return utils.query_all(conn, sql, (user_id,))


def insert_trip(conn, trip: schema.TripCreate, user_id: str) -> str:
    sql = f"""
        INSERT INTO {settings.TABLE_TRIPS}
            (trip_title, description, leader_id, start_datetime, end_datetime, trip_type, meeting_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    """
    result = utils.query_one(conn, sql, (
        trip.trip_title, trip.description, user_id,
        trip.start_datetime, trip.end_datetime, trip.trip_type, trip.meeting_location,
    ))
    return result["trip_id"]


def add_trip_member(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        INSERT INTO {settings.TABLE_TRIP_MEMBERS} (trip_id, user_id)
        VALUES (%s, %s)
        ON CONFLICT Do NOTHING
    """
    utils.execute(conn, sql, (trip_id, user_id))


def update_trip(conn, trip_id: str, trip: schema.TripUpdate) -> None:
    sql = f"""
        UPDATE {settings.TABLE_TRIPS}
        SET 
            trip_title=%s, 
            description=%s, 
            start_datetime=%s,
            end_datetime=%s, 
            trip_type=%s, 
            meeting_location=%s
        WHERE trip_id = %s
    """
    utils.execute(conn, sql, (
        trip.trip_title, trip.description, trip.start_datetime,
        trip.end_datetime, trip.trip_type, trip.meeting_location, trip_id,
    ))


def delete_trip(conn, trip_id: str) -> None:
    sql = f"""
        DELETE FROM {settings.TABLE_TRIPS} 
        WHERE trip_id = %s
    """
    utils.execute(conn, sql, (trip_id,))


def delete_trip_member(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        DELETE FROM {settings.TABLE_TRIP_MEMBERS} 
        WHERE trip_id = %s AND user_id = %s
    """
    utils.execute(conn, sql, (trip_id, user_id))


def update_trip_leader(conn, trip_id: str, user_id: str) -> None:
    sql = f"""
        UPDATE {settings.TABLE_TRIPS} 
        SET leader_id = %s 
        WHERE trip_id = %s
    """

    utils.execute(conn, sql, (user_id, trip_id))



def get_user_ongoing_trip(conn, user_id):
    sql = f"""
        SELECT *
        FROM {settings.TABLE_TRIPS} t
        JOIN {settings.TABLE_TRIP_MEMBERS} tm
            ON t.trip_id = tm.trip_id
        WHERE
            tm.user_id = %s
            AND NOW() BETWEEN t.start_datetime AND t.end_datetime
        """
    return utils.query_all(conn, sql, (user_id,))



def select_user_all_trips(conn, user_id: str):
    sql = f"""
        SELECT *
        FROM {settings.TABLE_TRIP_MEMBERS} tm
        JOIN {settings.TABLE_TRIPS} t 
            ON tm.trip_id = t.trip_id
        WHERE tm.user_id = %s
    """
    return utils.query_all(conn, sql, (user_id,))





def select_trip(conn, joining_trip_id: str):
    sql = f"""
        SELECT * FROM {settings.TABLE_TRIPS}
        WHERE trip_id = %s
    """

    return utils.query_all(conn, sql, (joining_trip_id,))


def insert_location_history(
    conn,
    trip_id: str,
    user_id: str,
    locations: list[schema.LocationPoint],
) -> None:
    if not locations:
        return

    values = []
    params = []
    for loc in locations:
        values.append("(%s, %s, %s, %s, COALESCE(%s, NOW()))")
        params.extend([
            trip_id,
            user_id,
            loc.latitude,
            loc.longitude,
            loc.timestamp,
        ])

    sql = f"""
        INSERT INTO {settings.TABLE_LOCATION_HISTORY}
            (trip_id, user_id, latitude, longitude, timestamp)
        VALUES {', '.join(values)}
    """
    utils.execute(conn, sql, params)
