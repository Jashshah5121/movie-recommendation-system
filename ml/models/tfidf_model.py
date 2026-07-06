import pandas as pd
import pickle

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).parent.parent

DATASET = BASE_DIR / "preprocessing" / "combined_features.csv"

EMBEDDINGS = BASE_DIR / "embeddings"

MOVIES_FILE = EMBEDDINGS / "movies.pkl"

SIMILARITY_FILE = EMBEDDINGS / "similarity.pkl"

VECTORIZER_FILE = EMBEDDINGS / "tfidf_vectorizer.pkl"


print("=" * 60)
print("Loading Dataset...")

movies = pd.read_csv(DATASET)

print(f"{len(movies)} movies loaded")

movies["tfidf_features"] = movies["tfidf_features"].fillna("")

print()
print("=" * 60)
print("Training TF-IDF...")


vectorizer = TfidfVectorizer(

    stop_words="english",

    max_features=25000,

    ngram_range=(1, 2),

    min_df=2

)


tfidf_matrix = vectorizer.fit_transform(

    movies["tfidf_features"]

)


print("Vocabulary Size :", len(vectorizer.vocabulary_))

print()
print("=" * 60)
print("Computing Similarity Matrix...")

similarity = cosine_similarity(

    tfidf_matrix

)

print("Similarity Shape :", similarity.shape)

print()
print("=" * 60)
print("Saving Models...")

with open(MOVIES_FILE, "wb") as f:

    pickle.dump(movies, f)

with open(SIMILARITY_FILE, "wb") as f:

    pickle.dump(similarity, f)

with open(VECTORIZER_FILE, "wb") as f:

    pickle.dump(vectorizer, f)

print()
print("Training Complete!")
print("movies.pkl")
print("similarity.pkl")
print("tfidf_vectorizer.pkl")
print("=" * 60)