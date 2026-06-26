from database import config, utils



def select_all_trips(conn):
    sql = f"""
        SELECT * FROM { config.TABLE_TRIPS }
    """

    return utils.query_all(conn, sql)



def select_user_participated_trips(conn, user_id: str):
    sql = f"""
        SELECT t.*, COUNT(tm.user_id) as member_count
        FROM { config.TABLE_TRIP_MEMBERS } t
        JOIN trip_members tm ON t.trip_id = tm.trip_id
        WHERE tm.user_id = %s
    """
    
    params = (user_id, )

    return utils.query_all(conn, sql, params)