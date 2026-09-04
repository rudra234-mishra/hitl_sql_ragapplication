import os
from psycopg2.pool import ThreadedConnectionPool
import psycopg2
from dotenv import load_dotenv
load_dotenv()
from logging_config import logger
import threading


_pool=None
_pool_lock=threading.Lock()

def _getpool():
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool=ThreadedConnectionPool(
                    minconn=2,
                    maxconn=20,
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    port=os.getenv("DB_PORT")
                )

    return _pool


def database_conn():
    try:
        logger.info("connection fetching from borrow :")
        conn=_getpool().getconn()
        logger.info("connection fetch successfully :")

        return conn

    except Exception as e:
        logger.error("failed to fetch connection from borrow :%s",e)



def release_connection(conn):
    try:
        if conn:
            pool=_getpool()
            pool.putconn(conn)

        logger.info("connection pass to borrow :")

    except Exception as e:
        logger.error("connection is not pass :%s",e)

    

