from contextlib import contextmanager
from collections.abc import Generator
from psycopg2.pool import ThreadedConnectionPool
from core.config import settings
import threading

_pool = None
_lock = threading.Lock()

def get_pool():
    global _pool
    if _pool is None:
        with _lock:
            if _pool is None:
                _pool = ThreadedConnectionPool(
                    settings.DB_MIN_CONN,
                    settings.DB_MAX_CONN,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    dbname=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD
                )
    return _pool


def get_conn():
    try:
        conn = get_pool().getconn()
        conn.autocommit = True
        return conn
    except Exception as e:
        print("❌ DB getconn 失敗:", e)
        raise


def release_conn(conn):
    if _pool is not None:
        _pool.putconn(conn)


@contextmanager
def conn_context() -> Generator:
    conn = None
    try:
        conn = get_conn()
        yield conn
    finally:
        if conn:
            release_conn(conn)


def close_pool():
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None