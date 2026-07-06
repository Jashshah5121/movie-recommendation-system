print("enrich.py started")
from dotenv import load_dotenv
import os
import time

from client import TMDBClient
from database import get_connection
from extractors import extract_movie_data

load_dotenv("../../backend/.env")

TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

client = TMDBClient(TOKEN)

BATCH_SIZE = 50


def enrich_movies(limit=None):

    conn = get_connection()
    cursor = conn.cursor()

    if limit:
        cursor.execute(
            """
            SELECT id
            FROM movies
            WHERE scraped = 0
            LIMIT ?
            """,
            (limit,)
        )
    else:
        cursor.execute(
            """
            SELECT id
            FROM movies
            WHERE scraped = 0
            """
        )

    movies = cursor.fetchall()

    total = len(movies)

    print("=" * 70)
    print(f"Movies to Enrich : {total}")
    print("=" * 70)

    success = 0
    failed = 0

    start_time = time.time()

    for index, (movie_id,) in enumerate(movies, start=1):

        movie_start = time.time()

        try:

            details = client.get_movie_details(movie_id)
            credits = client.get_movie_credits(movie_id)
            keywords = client.get_movie_keywords(movie_id)
            videos = client.get_movie_videos(movie_id)

            if (
                details is None
                or credits is None
                or keywords is None
                or videos is None
            ):
                print(f"[{index}/{total}] Skipped Movie ID {movie_id}")
                failed += 1
                continue

            movie = {

                "id": details["id"],
                "title": details["title"],
                "overview": details["overview"],
                "original_language": details["original_language"],
                "release_date": details["release_date"],
                "vote_average": details["vote_average"],
                "vote_count": details["vote_count"],
                "popularity": details["popularity"],
                "poster_path": details["poster_path"],
                "backdrop_path": details["backdrop_path"],
                "adult": details["adult"]

            }

            data = extract_movie_data(
                movie,
                details,
                credits,
                keywords,
                videos
            )

            cursor.execute(
                """
                UPDATE movies
                SET

                    overview=?,
                    genres=?,
                    keywords=?,
                    movie_cast=?,
                    director=?,
                    language=?,
                    release_date=?,
                    runtime=?,
                    rating=?,
                    vote_count=?,
                    popularity=?,
                    poster=?,
                    backdrop=?,
                    trailer=?,
                    production_companies=?,
                    production_countries=?,
                    collection=?,
                    tagline=?,
                    adult=?,
                    scraped=1

                WHERE id=?
                """,
                (
                    data["overview"],
                    data["genres"],
                    data["keywords"],
                    data["movie_cast"],
                    data["director"],
                    data["language"],
                    data["release_date"],
                    data["runtime"],
                    data["rating"],
                    data["vote_count"],
                    data["popularity"],
                    data["poster"],
                    data["backdrop"],
                    data["trailer"],
                    data["production_companies"],
                    data["production_countries"],
                    data["collection"],
                    data["tagline"],
                    int(data["adult"]),
                    data["id"]
                )
            )

            success += 1

            if success % BATCH_SIZE == 0:
                conn.commit()

            elapsed = time.time() - start_time

            avg = elapsed / index

            remaining = total - index

            eta = avg * remaining

            print(
                f"[{index}/{total}] "
                f"✓ {data['title'][:45]:45} "
                f"| ETA {eta/60:.1f} min"
            )

        except Exception as e:

            failed += 1

            print(
                f"[{index}/{total}] ✗ Movie ID {movie_id}"
            )

            print(e)

            continue

    conn.commit()

    conn.close()

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("ENRICHMENT COMPLETE")
    print("=" * 70)

    print(f"Successful : {success}")
    print(f"Failed     : {failed}")
    print(f"Total Time : {total_time/60:.2f} minutes")


if __name__ == "__main__":
    print("Starting enrichment...")
    enrich_movies()