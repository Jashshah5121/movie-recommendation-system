from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    title,
    language,
    rating,
    popularity
FROM movies
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()