import psycopg2
import pandas as pd

class PostgresConnector:
    def __init__(self, host, port, database, user, password):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=host, port=port, database=database, user=user, password=password
            )
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def fetch_query(self, query):
        if self.conn is None:
            print("No active database connection.")
            return None
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
