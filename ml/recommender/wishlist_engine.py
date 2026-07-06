from recommender.utils import get_movies
from recommender.hybrid_ranker import hybrid_recommend


def recommend_from_wishlist(movie_ids, top_k=20):
    """
    Generate recommendations based on the user's wishlist.
    """

    movies = get_movies()

    wishlist = movies[movies["id"].isin(movie_ids)]

    if wishlist.empty:
        return []

    # Combine all wishlist movie titles
    query = " ".join(wishlist["title"].tolist())

    result = hybrid_recommend(query, top_k)

    recommendations = result["results"]

    # Remove movies already in wishlist
    recommendations = [
        movie
        for movie in recommendations
        if movie["id"] not in movie_ids
    ]

    return recommendations