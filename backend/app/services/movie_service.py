from pathlib import Path
import sqlite3
import requests
import os

from app.utils.movie_formatter import format_movie
from app.core.config import settings

# 1. Check if we are running inside the Docker container
if os.path.exists("/app/ml/dataset/movies.db"):
    DB_PATH = "/app/ml/dataset/movies.db"
    
# 2. Otherwise, use your original logic for local Windows development
else:
    ROOT_DIR = Path(__file__).resolve().parents[3]
    DB_PATH = ROOT_DIR / "ml" / "dataset" / "movies.db"


class MovieService:     

    @staticmethod
    def autocomplete(query):
        try:
            url = "https://api.themoviedb.org/3/search/movie"

            headers = {
                "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}",
                "accept": "application/json",
            }

            response = requests.get(
                url,
                headers=headers,
                params={
                    "query": query,
                    "page": 1,
                },
            )

            print(response.status_code)
            print(response.text)

            if response.status_code != 200:
                return []

            movies = response.json()["results"][:8]

            return [
                {
                    "id": m["id"],
                    "title": m["title"],
                    "year": m.get("release_date", "")[:4] if m.get("release_date") else "",
                    "poster": (
                        f"https://image.tmdb.org/t/p/w200{m['poster_path']}"
                        if m.get("poster_path")
                        else None
                    ),
                }
                for m in movies
            ]
            
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_movie(movie_id: int):

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM movies
            WHERE id = ?
            """,
            (movie_id,)
        )

        movie = cursor.fetchone()

        conn.close()

        if movie is None:
            return None

        return format_movie(dict(movie))


    @staticmethod
    def get_onboarding_movies(languages=None, genres=None, limit=60):

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM movies
        WHERE 1=1
        """

        params = []

        # -----------------------------
        # Multiple Language Filter
        # -----------------------------
        if languages:
            sql += " AND ("
            conditions = []
            for lang in languages:
                conditions.append("language = ?")
                params.append(lang)
            sql += " OR ".join(conditions)
            sql += ")"

        # -----------------------------
        # Genre Filter
        # -----------------------------
        if genres:
            sql += " AND ("
            conditions = []
            for genre in genres:
                conditions.append("genres LIKE ?")
                params.append(f"%{genre}%")
            sql += " OR ".join(conditions)
            sql += ")"

        sql += """
        ORDER BY
            popularity DESC,
            rating DESC,
            vote_count DESC
        LIMIT ?
        """

        params.append(limit)

        cursor.execute(sql, params)
        movies = cursor.fetchall()
        conn.close()

        return [
            format_movie(dict(movie))
            for movie in movies
        ]