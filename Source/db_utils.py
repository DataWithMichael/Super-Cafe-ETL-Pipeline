import psycopg2
from psycopg2.extras import execute_batch
from contextlib import contextmanager

@contextmanager
def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="postgres",
        password="secret",
        port=5432
    )
    try:
        yield conn
    finally:
        conn.close()

def run_batch_insert(query, records):
    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
