from database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT
title,
genres,
movie_cast,
director,
runtime,
keywords
FROM movies
WHERE scraped=1
LIMIT 5
""")

for row in cursor.fetchall():

    print("="*60)

    print("Title      :", row[0])

    print("Genres     :", row[1])

    print("Cast       :", row[2])

    print("Director   :", row[3])

    print("Runtime    :", row[4])

    print("Keywords   :", row[5])

conn.close()