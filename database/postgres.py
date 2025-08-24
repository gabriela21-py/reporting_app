import pandas as pd
import psycopg2
from database.db_interface import DatabaseInterface

import os

host = os.getenv("HOST", "localhost")
db = os.getenv("DATABASE", "dbname")
user = os.getenv("USER", "user")
password = os.getenv("PASSWORD", "password")


class PostgresDatabase(DatabaseInterface):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=host,
            database=db,
            user=user,
            password=password
        )
    def get_data(self, query: str) ->  pd.DataFrame:
        return pd.read_sql(query, self.conn)
