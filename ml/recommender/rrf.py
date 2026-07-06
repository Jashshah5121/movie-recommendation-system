from recommender.semantic_engine import semantic_search 
from recommender.bm25_engine import bm25_search


K = 60


def reciprocal_rank_fusion(*rankings):

    scores = {}

    for ranking in rankings:

        for rank, movie in enumerate(ranking, start=1):

            movie_id = movie["id"]

            if movie_id not in scores:

                scores[movie_id] = {

                    "movie": movie,

                    "score": 0.0,

                    "sources": []

                }

            scores[movie_id]["score"] += 1 / (K + rank)

            scores[movie_id]["sources"].append(
                movie["source"]
            )

    fused = []

    for item in scores.values():

        movie = item["movie"].copy()

        movie["score"] = round(item["score"], 6)

        movie["sources"] = sorted(
            list(set(item["sources"]))
        )

        fused.append(movie)

    fused.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return fused


def hybrid_search(query, top_k=10):

    semantic = semantic_search(

        query,

        top_k=20

    )

    bm25 = bm25_search(

        query,

        top_k=20

    )

    fused = reciprocal_rank_fusion(

        semantic,

        bm25

    )

    return fused[:top_k]