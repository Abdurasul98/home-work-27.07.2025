import psycopg2
from psycopg2.extras import DictCursor
from core.database import get_db_conn

tasks = """
CREATE TABLE IF NOT EXISTS home_work_27_07_2025 
(
    id SERIAL PRIMARY KEY,
    employee_name VARCHAR(128) NOT NULL,
    month VARCHAR(32) NOT NULL,
    base_salary DECIMAL(10,2) NOT NULL,
    bonus DECIMAL(10,2) DEFAULT 0,
    penalty DECIMAL(10,2) DEFAULT 0,
    net_salary DECIMAL(10,2),
    status VARCHAR(128) CHECK (status IN ('paid','pending','delayed'))
);
"""


def create_tables():
    try:
        conn = get_db_conn()
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute(tasks)
        conn.commit()

        conn.close()
        cursor.close()
        return True
    except psycopg2.OperationalError as e:
        print(e)
        return None