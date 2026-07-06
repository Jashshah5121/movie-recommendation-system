from recommender.fuzzy_search import resolve_movie
from recommender.query_classifier import classify_query
from recommender.rrf import hybrid_search
from recommender.recommendation_engine import recommend

def get_threshold(query):

    words = len(query.split())

    if words <= 2:
        return 60

    if words <= 4:
        return 70

    return 90


def search(query, top_k=10):

    classification = classify_query(query)

    # Only attempt RapidFuzz if it looks like a movie title
    if classification["type"] == "movie_title":

        movie = resolve_movie(
            query,
            threshold=get_threshold(query)
        )

        if movie is not None:

            recommendations = recommend(
            movie["title"],
            top_k=10
        )

        return {

        "type": "movie",

        "query": query,

        "resolved": movie,

        "recommendations": recommendations

    }

    # Otherwise use hybrid search
    results = hybrid_search(
        query,
        top_k=top_k
    )

    return {

        "type": "search",

        "query": query,

        "resolved": None,

        "results": results

    }