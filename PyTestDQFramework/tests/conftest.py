import pytest
from src.connectors.postgres.postgres_connector import PostgresConnector

@pytest.fixture(scope='session')
def pg_conn():
    conn = None
    try:
        conn = PostgresConnector(
            host="localhost",
            port=5432,
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        yield conn
    except Exception as e:
        print(f"Error connecting to Postgres: {e}")
        raise
    finally:
        if conn:
            conn.close()
