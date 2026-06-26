# from psycopg2.extras import RealDictCursor


# def query_all(conn, sql, params=None):

#     with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#         cursor.execute(sql, params)
#         return cursor.fetchall()


# def query_one(conn, sql, params=None):

#     with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#         cursor.execute(sql, params)
#         return cursor.fetchone()


# def execute(conn, sql, params=None):

#     with conn.cursor() as cursor:
#         cursor.execute(sql, params)