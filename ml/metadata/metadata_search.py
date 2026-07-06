import pandas as pd
from recommender.utils import get_movies

movies = get_movies()


class MetadataSearch:

    @staticmethod
    def _clean(value):
        if pd.isna(value):
            return ""

        return str(value).lower().strip()

    @staticmethod
    def search(query, top_k=20):

        query = query.lower().strip()

        results = []

        for _, movie in movies.iterrows():

            score = 0
            why = []

            # -----------------------------
            # Dataset Fields
            # -----------------------------

            director = MetadataSearch._clean(
                movie.get("director")
            )

            cast = MetadataSearch._clean(
                movie.get("movie_cast")
            )

            genres = MetadataSearch._clean(
                movie.get("genres_list")
            )

            keywords = MetadataSearch._clean(
                movie.get("keywords_list")
            )

            companies = MetadataSearch._clean(
                movie.get("production_companies")
            )

            countries = MetadataSearch._clean(
                movie.get("production_countries")
            )

            collection = MetadataSearch._clean(
                movie.get("collection")
            )

            language = MetadataSearch._clean(
                movie.get("language")
            )

            year = MetadataSearch._clean(
                movie.get("year")
            )

            # -----------------------------
            # Matching
            # -----------------------------

            if query in director:
                score += 5
                why.append("Director")

            if query in cast:
                score += 5
                why.append("Actor")

            if query in genres:
                score += 3
                why.append("Genre")

            if query in keywords:
                score += 3
                why.append("Keyword")

            if query in companies:
                score += 2
                why.append("Studio")

            if query in countries:
                score += 2
                why.append("Country")

            if query in collection:
                score += 2
                why.append("Collection")

            if query == language:
                score += 1
                why.append("Language")

            if query == year:
                score += 2
                why.append("Year")

            if score > 0:

                results.append({

                    "id": int(movie["id"]),

                    "title": movie["title"],

                    "poster": movie["poster"],

                    "rating": float(movie["rating"]),

                    "year": int(movie["year"]) if pd.notna(movie["year"]) else None,

                    "score": score,

                    "source": "metadata",

                    "why": why

                })

        results.sort(

            key=lambda x: (

                x["score"],

                x["rating"]

            ),

            reverse=True

        )

        return results[:top_k]