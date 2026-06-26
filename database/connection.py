# from psycopg2.pool import ThreadedConnectionPool

# from database.config import settings

# _pool = None

# def get_pool():
#     global _pool
#     if _pool is None:
#         _pool = ThreadedConnectionPool(
#             settings.DB_MIN_CONN,
#             settings.DB_MAX_CONN,
#             host=settings.DB_HOST,
#             port=settings.DB_PORT,
#             dbname=settings.DB_NAME,
#             user=settings.DB_USER,
#             password=settings.DB_PASSWORD
#         )
#     return _pool


# def get_conn():
#     conn = get_pool().getconn()
#     conn.autocommit = True
#     return conn


# def release_conn(conn):
#     if _pool is not None:
#         _pool.putconn(conn)