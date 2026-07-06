from collections import defaultdict

from recommender.recommendation_engine import recommend
from recommender.utils import get_movies

movies_df = get_movies()


def recommend_from_onboarding(
    selected_movies,
    genres,
    languages,
    top_k=20,
):
    scores = defaultdict(float)

    selected_ids = set(selected_movies)

    for movie_id in selected_movies:

        movie = movies_df[movies_df["id"] == movie_id]

        if movie.empty:
            continue

        title = movie.iloc[0]["title"]

        recommendations = recommend(title, top_k=20)

        for rec in recommendations:

            if rec["id"] in selected_ids:
                continue

            score = rec.get("score", 0)

            rec_movie = movies_df[movies_df["id"] == rec["id"]]

            if rec_movie.empty:
                continue

            rec_movie = rec_movie.iloc[0]

            # Genre Boost

            rec_genres = str(rec_movie["genres"]).lower()

            for g in genres:
                if g.lower() in rec_genres:
                    score += 2

            # Language Boost

            if rec_movie["language"] in languages:
                score += 1

            scores[rec["id"]] += score

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for movie_id, score in ranked[:top_k]:

        movie = movies_df[movies_df["id"] == movie_id].iloc[0]

        results.append({
            "id": int(movie["id"]),
            "title": movie["title"],
            "poster": movie["poster"],
            "rating": float(movie["rating"]),
            "year": int(movie["year"]) if movie["year"] else None,
            "score": round(score, 2),
        })

    return results