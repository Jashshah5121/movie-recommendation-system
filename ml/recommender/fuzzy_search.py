from rapidfuzz import process, fuzz
from recommender.utils import get_movies
import pandas as pd


print("Loading movies...")

movies = get_movies()

titles = movies["title"].fillna("").tolist()


def resolve_movie(query, threshold=70):

    result = process.extractOne(
        query,
        titles,
        scorer=fuzz.WRatio
    )

    print("Query :", query)
    print("Result:", result)

    if result is None:
        return None

    title, score, index = result

    print("Title :", title)
    print("Score :", score)

    if score < threshold:
        return None

    movie = movies.iloc[index]

    year = None

    if pd.notna(movie["year"]):
        year = int(movie["year"])

    return {

        "id": int(movie["id"]),

        "title": movie["title"],

        "poster": movie["poster"],

        "backdrop": movie["backdrop"],

        "rating": float(movie["rating"]),

        "language": movie["language"],

        "year": year,

        "score": round(float(score), 2),

        "source": "fuzzy",

        "why": []

    }