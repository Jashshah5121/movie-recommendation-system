import pickle
import numpy as np
import pandas as pd

from pathlib import Path
from sentence_transformers import SentenceTransformer

from recommender.utils import get_movies

BASE_DIR = Path(__file__).parent.parent

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

INDEX_FILE = EMBEDDINGS_DIR / "semantic_index.pkl"


print("Loading semantic engine...")

movies = get_movies()

with open(INDEX_FILE, "rb") as f:
    index = pickle.load(f)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def semantic_search(query, top_k=10):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.kneighbors(
        query_embedding,
        n_neighbors=top_k
    )

    recommendations = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        movie = movies.iloc[idx]

        recommendations.append({

            "id": int(movie["id"]),

            "title": movie["title"],

            "poster": movie["poster"],

            "rating": float(movie["rating"]),

            "year": int(movie["year"]) if pd.notna(movie["year"]) else None,

            "score": round(
                1 - float(distance),
                3
            ),

            "source": "semantic",

            "why": []

        })

    return recommendations