import pandas as pd

from .embedding_loader import EmbeddingLoader


EmbeddingLoader.load()


def semantic_search(query, top_k=10):

    model = EmbeddingLoader.model

    index = EmbeddingLoader.index

    movies = EmbeddingLoader.movies

    query_embedding = model.encode(

        [query],

        convert_to_numpy=True

    )

    distances, indices = index.kneighbors(

        query_embedding,

        n_neighbors=top_k

    )

    results = []

    for distance, idx in zip(

        distances[0],

        indices[0]

    ):

        movie = movies.iloc[idx]

        results.append({

            "id": int(movie["id"]),

            "title": movie["title"],

            "poster": movie["poster"],

            "rating": float(movie["rating"]),

            "year": int(movie["year"]) if pd.notna(movie["year"]) else None,

            "score": round(

                1 - float(distance),

                4

            ),

            "source": "semantic"

        })

    return results