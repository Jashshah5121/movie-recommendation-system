from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM movies")
print("Total Movies:", cursor.fetchone()[0])

conn.close()