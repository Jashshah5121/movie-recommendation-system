from pathlib import Path
import sqlite3
import os
from app.utils.movie_formatter import format_movie


# 1. Check if we are running inside the Docker container
if os.path.exists("/app/ml/dataset/movies.db"):
    DB_PATH = "/app/ml/dataset/movies.db"
    
# 2. Otherwise, use your original logic for local Windows development
else:
    ROOT_DIR = Path(__file__).resolve().parents[3]
    DB_PATH = ROOT_DIR / "ml" / "dataset" / "movies.db"


class DiscoverService:

    @staticmethod
    def discover(

        genre=None,

        language=None,

        from_year=None,

        to_year=None,

        min_rating=None,

        max_runtime=None,

        sort="popularity",

        page=1,

        limit=20

    ):

        conn = sqlite3.connect(DB_PATH)

        conn.row_factory = sqlite3.Row

        query = """
        SELECT *
        FROM movies
        WHERE scraped = 1
        """

        params = []

        # ----------------------------------------------------
        # Genre Filter
        # ----------------------------------------------------

        if genre:

            genres = [

                g.strip()

                for g in genre.split(",")

                if g.strip()

            ]

            if genres:

                query += " AND ("

                query += " OR ".join(

                    ["genres LIKE ?"] * len(genres)

                )

                query += ")"

                params.extend(

                    [f"%{g}%" for g in genres]

                )

        # ----------------------------------------------------
        # Language
        # ----------------------------------------------------

        if language:

            query += " AND LOWER(language)=LOWER(?)"

            params.append(language)

        # ----------------------------------------------------
        # Rating
        # ----------------------------------------------------

        if min_rating is not None:

            query += " AND rating >= ?"

            params.append(min_rating)

        # ----------------------------------------------------
        # Runtime
        # ----------------------------------------------------

        if max_runtime is not None:

            query += " AND runtime <= ?"

            params.append(max_runtime)

        # ----------------------------------------------------
        # Year Range
        # ----------------------------------------------------

        if from_year is not None:

            query += " AND CAST(substr(release_date,1,4) AS INTEGER) >= ?"

            params.append(from_year)

        if to_year is not None:

            query += " AND CAST(substr(release_date,1,4) AS INTEGER) <= ?"

            params.append(to_year)

        # ----------------------------------------------------
        # Sorting
        # ----------------------------------------------------

        sort_columns = {

            "popularity": "popularity DESC",

            "rating": "rating DESC",

            "newest": "release_date DESC",

            "oldest": "release_date ASC"

        }

        query += f"""

        ORDER BY

        {sort_columns.get(sort, "popularity DESC")}

        """

        # ----------------------------------------------------
        # Pagination
        # ----------------------------------------------------

        offset = (page - 1) * limit

        query += """

        LIMIT ?

        OFFSET ?

        """

        params.extend([limit, offset])

        cursor = conn.cursor()

        cursor.execute(query, params)

        movies = cursor.fetchall()

        conn.close()

        return [

            format_movie(dict(movie))

            for movie in movies

        ]