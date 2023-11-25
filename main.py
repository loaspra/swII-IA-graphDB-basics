from scripts.PsycoClient import PostgresClient

# Usage example
t_client = PostgresClient()
t_client.connect_to_database()
result = t_client.consult_table_data("movies")
resultLinks = t_client.consult_table_data("links")
resultRatings = t_client.consult_table_data("ratings")
resultTags = t_client.consult_table_data("tags")
print(result)
print(resultLinks)
print(resultRatings)
print(resultTags)