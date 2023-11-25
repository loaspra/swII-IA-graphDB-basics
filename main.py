from scripts.PsycoClient import PostgresClient
from scripts.ChromaInserter import ChromaInserter


p_client = PostgresClient()
p_client.connect_to_database()

# Run only once (NOT RUN)
# p_client.create_tables()
tables = ["links", "movies", "ratings", "tags"]
path = "./data/ml-latest-small/"
# p_client.insert_csv_data(tables, path)

# Testing
result = p_client.consult_table_data("movies")
print(result)
resultLinks = p_client.consult_table_data("links")
print(resultLinks)
resultRatings = p_client.consult_table_data("ratings")
print(resultRatings)
resultTags = p_client.consult_table_data("tags")
print(resultTags)


# Final Query
SQL_avg_rating = "SELECT movieId, SUM(RATING)/COUNT(*) as AVG_RATING FROM ratings GROUP BY movieId"

SQL_tags_cat = "SELECT movieId, STRING_AGG(tag, ' ') FROM tags GROUP BY movieId"

SQL_movies = "SELECT movieId as mainMovieId, title, genres FROM movies"

QUERY = f"""
SELECT mvTcat.title, mvTcat.genres, rate.AVG_RATING, mvTcat.STRING_AGG
FROM
(
    ({SQL_movies}) mv
    JOIN ({SQL_tags_cat}) tcat
    ON mv.mainMovieId = tcat.movieId
) mvTcat
JOIN ({SQL_avg_rating}) rate
ON mvTcat.mainMovieId = rate.movieId;
"""

result = p_client.safe_execute(QUERY)
print(len(result))

final_data = list(map(lambda x: " ".join([str(k) for k in list(x)]), result))
print(len(final_data))

chroma_inserter = ChromaInserter()
chroma_inserter.insert_final_data(final_data)