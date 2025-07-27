import psycopg2

from core.config import db_config

def get_db_conn():
    try:
        conn = psycopg2.connect(**db_config)
        return conn

    except Exception as e:
        print(e)
        return None