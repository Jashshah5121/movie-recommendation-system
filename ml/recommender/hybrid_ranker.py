from recommender.search_router import search
from recommender.explain import generate_explanation


def hybrid_recommend(query, top_k=10):
    """
    Intelligent recommendation entry point.

    Movie title
        -> Fuzzy Search
        -> Recommendation Engine

    Natural language
        -> BM25
        -> Semantic Search
        -> RRF Fusion
    """

    result = search(query, top_k)

    # ------------------------
    # Movie Recommendation Mode
    # ------------------------
    if result["type"] == "movie":

        recommendations = result["recommendations"]

        for movie in recommendations:
            movie["why"] = generate_explanation(
                movie,
                query=result["query"]
            )

            score = movie.get("score", 0)
            movie["match"] = f"{round(score * 100)}%"

        return {
            "mode": "movie",
            "query": result["query"],
            "resolved": result["resolved"],
            "count": len(recommendations),
            "results": recommendations
        }

    # ------------------------
    # Hybrid Search Mode
    # ------------------------
    recommendations = result["results"]

    for movie in recommendations:
        movie["why"] = generate_explanation(
            movie,
            query=result["query"]
        )

        score = movie.get("score", 0)
        movie["match"] = f"{round(score * 100)}%"

    return {
        "mode": "hybrid",
        "query": result["query"],
        "resolved": None,
        "count": len(recommendations),
        "results": recommendations
    }