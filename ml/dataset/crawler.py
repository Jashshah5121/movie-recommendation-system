from client import TMDBClient
from database import get_connection

from dotenv import load_dotenv
import os

print("Crawler started")

load_dotenv("../../backend/.env")

TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

print("Token found:", TOKEN is not None)

client = TMDBClient(TOKEN)


START_YEAR = 1989
END_YEAR = 2026
PAGES_PER_YEAR = 10



def save_movies(year, pages):

    conn = get_connection()
    cursor = conn.cursor()

    total = 0

    for page in range(1, pages + 1):

        print(f"\nYear {year} | Page {page}")

        data = client.discover_movies(
            year=year,
            page=page
        )

        if data is None:
            continue

        inserted = 0

        for movie in data["results"]:

            cursor.execute(
                """
                INSERT OR IGNORE INTO movies(

                    id,
                    title,
                    overview,
                    language,
                    release_date,
                    rating,
                    vote_count,
                    popularity,
                    poster,
                    backdrop,
                    adult

                )

                VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """,

                (

                    movie["id"],
                    movie["title"],
                    movie["overview"],
                    movie["original_language"],
                    movie["release_date"],
                    movie["vote_average"],
                    movie["vote_count"],
                    movie["popularity"],
                    movie["poster_path"],
                    movie["backdrop_path"],
                    int(movie["adult"])

                )
            )

            if cursor.rowcount > 0:
                inserted += 1

        conn.commit()

        total += inserted

        print(f"Inserted this page : {inserted}")
        print(f"Total inserted     : {total}")

    conn.close()

    print(f"\nFinished Year {year}")



if __name__ == "__main__":

    print("Main block executing\n")

    for year in range(END_YEAR, START_YEAR - 1, -1):

        print("=" * 60)
        print(f"Starting Year {year}")
        print("=" * 60)

        save_movies(
            year=year,
            pages=PAGES_PER_YEAR
        )

    print("\nAll years completed!")