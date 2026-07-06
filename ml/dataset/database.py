import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "movies.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (

            id INTEGER PRIMARY KEY,

        title TEXT,

        overview TEXT,

        genres TEXT,

        keywords TEXT,

        movie_cast TEXT,

        director TEXT,

        language TEXT,

        release_date TEXT,

        runtime INTEGER,

        rating REAL,

        vote_count INTEGER,

        popularity REAL,

        poster TEXT,

        backdrop TEXT,

        trailer TEXT,

        production_companies TEXT,

        production_countries TEXT,

        collection TEXT,

        tagline TEXT,

        adult INTEGER,

        scraped INTEGER DEFAULT 0,

        last_updated TEXT

    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")