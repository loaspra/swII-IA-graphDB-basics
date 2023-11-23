from scripts.TursoClient import TursoClient

# Usage example
t_client = TursoClient()
t_client.connect_to_database()
# t_client.create_tables()
# t_client.insert_data()
t_client.consult_table_data("movies")