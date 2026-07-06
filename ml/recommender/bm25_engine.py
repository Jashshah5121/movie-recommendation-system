import pandas as pd
import numpy as np

from rank_bm25 import BM25Okapi

from recommender.utils import get_movies

print("Loading movies...")

movies = get_movies()

# -------------------------------------------------------
# Build Corpus
# -------------------------------------------------------

corpus = []

for text in movies["semantic_features"].fillna(""):

    corpus.append(text.lower().split())

bm25 = BM25Okapi(corpus)


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def clean(value):

    if pd.isna(value):
        return None

    return value


# -------------------------------------------------------
# Search
# -------------------------------------------------------

def bm25_search(query, top_k=10):

    tokens = query.lower().split()

    scores = bm25.get_scores(tokens)

    indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in indices:

        movie = movies.iloc[idx]

        results.append({

            "id": int(movie["id"]),

            "title": clean(movie["title"]),

            "poster": clean(movie["poster"]),

            "backdrop": clean(movie["backdrop"]),

            "rating": float(movie["rating"])
            if pd.notna(movie["rating"])
            else None,

            "language": clean(movie["language"]),

            "year": int(movie["year"])
            if pd.notna(movie["year"])
            else None,

            "score": round(float(scores[idx]), 3),

            "source": "bm25",

            "why": []

        })

    return results