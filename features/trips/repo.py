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

            COALESCE(
                json_agg(
                    json_build_object(
                        'user_id', u.user_id,
                        'display_name', u.display_name
                    )
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
            t.end_datetime;
    """
    
    params = (user_id, )

    return utils.query_all(conn, sql, params)



def insert_new_trips(conn, trip: schema.Trip):
    sql = f"""
        INSERT INTO { config.TABLE_TRIPS } (trip_title, description, leader_id, start_datetime, end_datetime, meeting_location)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING trip_id
    """
    
    params = (trip.trip_title, trip.description, trip.leader_id, trip.start_datetime, trip.end_datetime, trip.meeting_location)

    result =  utils.query_one(conn, sql, params)
    return result['trip_id']



def add_user_to_trip(conn, trip_id: str, user_id: str):
    sql = f"""
        INSERT INTO { config.TABLE_TRIP_MEMBERS } (trip_id, user_id)
        VALUES(%s, %s)
    """
    
    params = (trip_id, user_id)

    return utils.execute(conn, sql, params)





def delete_trip(conn, trip_id: str):
    sql = f"""
        DELETE FROM { config.TABLE_TRIPS }
        WHERE trip_id = %s
    """

    params = (trip_id, )
    return utils.execute(conn, sql, params)




def update_trip(conn, trip: schema.Trip, trip_id: str):
    sql = f"""
        UPDATE { config.TABLE_TRIPS } 
        SET 
            trip_title=%s,
            description=%s, 
            start_datetime=%s,
            end_datetime=%s,
            meeting_location=%s
        WHERE trip_id = %s
    """

    params = (trip.trip_title, trip.description, trip.start_datetime, trip.end_datetime, trip.meeting_location, trip_id)
    return utils.execute(conn, sql, params)





def delete_user_from_trip(conn, trip_id: str, user_id: str):
    sql = f"""
        DELETE FROM { config.TABLE_TRIP_MEMBERS }
        WHERE trip_id = %s and user_id =%s
    """

    params = (trip_id, user_id)
    return utils.execute(conn, sql, params)





def update_trip_leader(conn, trip_id, user_id):
    sql = f"""
        UPDATE { config.TABLE_TRIPS } 
        SET leader_id = %s
        WHERE trip_id = %s
    """

    params = (user_id, trip_id)
    return utils.execute(conn, sql, params)