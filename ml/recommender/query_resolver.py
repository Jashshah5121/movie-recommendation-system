import re

from recommender.utils import (
    get_movies,
    get_movie_index
)

movies = get_movies()


def resolve_query(intent_data):

    intent = intent_data["intent"]

    query = intent_data["query"].strip()

    # --------------------------
    # Exact Movie
    # --------------------------

    if intent == "EXACT_MOVIE":

        movie = movies[
            movies["title"].str.lower() == query.lower()
        ]

        if not movie.empty:

            movie = movie.iloc[0]

            return {

                "intent": intent,

                "movie": movie["title"],

                "movie_id": int(movie["id"])

            }

        return {

            "intent": "DESCRIPTION",

            "query": query

        }

    # --------------------------
    # Similar Movie
    # --------------------------

    if intent == "SIMILAR_MOVIE":

        title = re.sub(
            r"movies like|movie like|like",
            "",
            query,
            flags=re.IGNORECASE
        ).strip()

        return {

            "intent": intent,

            "movie": title

        }

    return {

        "intent": intent,

        "query": query

    }