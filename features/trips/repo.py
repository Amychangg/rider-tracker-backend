from database import config, utils
from features.trips import schema



def select_all_trips(conn):
    sql = f"""
        SELECT * FROM { config.TABLE_TRIPS }
    """

    return utils.query_all(conn, sql)



def select_trips_and_participated_users(conn, user_id: str):
    sql = f"""
        SELECT
            t.trip_id,
            t.trip_title,
            t.description,
            t.leader_id,
            t.start_datetime,
            t.end_datetime,
            t.trip_type,
            t.status,

            COALESCE(
                json_agg(
                    json_build_object(
                        'user_id', u.user_id,
                        'user_name', u.user_name,
                        'created_date', tm.created_date
                    )
                    ORDER BY tm.created_date
                ) FILTER (WHERE tm.user_id IS NOT NULL),
                '[]'
            ) AS members

        FROM trips t
        LEFT JOIN trip_members tm
            ON t.trip_id = tm.trip_id
        LEFT JOIN users u
            ON tm.user_id = u.user_id

        WHERE t.trip_id IN (
            SELECT trip_id
            FROM trip_members 
            WHERE user_id = %s
        )

        GROUP BY
            t.trip_id,
            t.trip_title,
            t.description,
            t.leader_id,
            t.start_datetime,
            t.end_datetime,
            t.trip_type,
            t.status;
    """
    
    params = (user_id, )

    return utils.query_all(conn, sql, params)



def insert_new_trips(conn, trip: schema.Trip):
    sql = f"""
        INSERT INTO { config.TABLE_TRIPS } (trip_title, description, leader_id, start_datetime, end_datetime, status, trip_type, meeting_location)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        
    """
    
    params = (trip.trip_title, trip.description, trip.leader_id, trip.start_datetime, trip.end_datetime, trip.status, trip.trip_type, trip.meeting_location)

    return utils.execute(conn, sql, params)