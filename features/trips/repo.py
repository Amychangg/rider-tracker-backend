from database import config, utils



def select_all_trips(conn):
    sql = f"""
        SELECT * FROM { config.TABLE_TRIPS }
    """

    return utils.query_all(conn, sql)

