from recommender.utils import (
    get_movies,
    get_similarity,
    get_movie_index
)


def recommend(title, top_k=10):

    movies = get_movies()

    similarity = get_similarity()

    movie_index = get_movie_index(title)

    if movie_index is None:

        return []

    distances = list(
        enumerate(similarity[movie_index])
    )

    distances.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, score in distances[1:top_k + 1]:

        movie = movies.iloc[index]

        recommendations.append({

            "id": int(movie["id"]),

            "title": movie["title"],

            "poster": movie["poster"],

            "rating": float(movie["rating"]),

            "score": float(score)

        })

    return recommendations