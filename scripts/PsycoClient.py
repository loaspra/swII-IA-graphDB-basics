import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from tqdm import tqdm

class PostgresClient:
    def __init__(self):
        super()
        self.connection = None

    def connect_to_database(self):
        if self.connection is None:
            # Load the environment variables from .env file
            load_dotenv()

            # Get the database credentials from environment variables
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")
            database = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")

            # Connect to the PostgreSQL database
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )

    def create_tables(self):
        queries = [
            """
            CREATE TABLE links (
                movieId INT,
                imdbId INT,
                tmdbId INT
            );
            """,
            """
            CREATE TABLE movies (
                movieId INT,
                title VARCHAR(255),
                genres VARCHAR(255)
            );
            """,
            """
            CREATE TABLE ratings (
                userId INT,
                movieId INT,
                rating FLOAT,
                timestamp INT
            );
            """,
            """
            CREATE TABLE tags (
                userId INT,
                movieId INT,
                tag VARCHAR(255),
                timestamp INT
            );
            """
        ]

        cursor = self.connection.cursor()
        for query in queries:
            cursor.execute(query)
        self.connection.commit()

    def insert_csv_data(self, tables, path):

        cursor = self.connection.cursor()
        for table in tables:
            df_table = pd.read_csv(f"{path}{table}.csv")
            columns = ", ".join(df_table.columns)
            values = []
            for row in tqdm(df_table.itertuples(index=False)):
                values.append([None if pd.isna(value) else value for value in row])
                if len(values) == 100:  # Batch size
                    placeholders = ", ".join(["%s"] * len(df_table.columns))
                    statement = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                    cursor.executemany(statement, values)
                    values = []
            if values:
                placeholders = ", ".join(["%s"] * len(df_table.columns))
                statement = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                cursor.executemany(statement, values)
        self.connection.commit()

    def consult_table_data(self, table):
        if self.connection is None:
            print("Client not connected")
            self.connect_to_database()

        print(f"Consulting table '{table}'")
        query = f"SELECT * FROM {table} LIMIT 10"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        return result_set
    
    def safe_execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()