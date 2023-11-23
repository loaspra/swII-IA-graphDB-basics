import os
from dotenv import load_dotenv
import libsql_client
import pandas as pd
from tqdm import tqdm

class TursoClient:
    def __init__(self):
        super()
        self.client = None

    def connect_to_database(self):
        if self.client is None:
            # Load the environment variables from .env file
            load_dotenv()

            # Get the token from the environment variable
            auth_token = os.getenv("AUTH_TOKEN")

            self.client = libsql_client.create_client_sync(
                url="libsql://awaited-human-fly-loaspra.turso.io",
                auth_token=auth_token
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

        for query in queries:
            result_set = self.client.execute(query)

    def insert_data(self):
        tables = ["links", "movies", "ratings", "tags"]

        for table in tables:
            df_table = pd.read_csv(f"./data/ml-latest-small/{table}.csv")
            statements = []
            values = []
            for row in tqdm(df_table.itertuples(index=False)):
                values.append([str(value) for value in row])
                if len(values) == 100:  # Batch size
                    statement = f"INSERT INTO {table} VALUES (?, ?, ?, ?)"  # Modify the statement accordingly
                    statements.append(libsql_client.Statement(statement, values))
                    values = []
            if values:
                statement = f"INSERT INTO {table} VALUES (?, ?, ?, ?)"  # Modify the statement accordingly
                statements.append(libsql_client.Statement(statement, values))
            rss = self.client.batch(statements)

    def consult_table_data(self, table):
        if self.client is None:
            print("Client not connected")
            self.connect_to_database()

        print(f"Consulting table '{table}'")
        query = f"SELECT * FROM {table} LIMIT 10"
        result_set = self.client.execute(query)
        return result_set