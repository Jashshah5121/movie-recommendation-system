from pathlib import Path
import pickle
import numpy as np


BASE_DIR = Path(__file__).parent.parent

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

MOVIES_PATH = EMBEDDINGS_DIR / "movies.pkl"
SIMILARITY_PATH = EMBEDDINGS_DIR / "similarity.pkl"
TFIDF_PATH = EMBEDDINGS_DIR / "tfidf_vectorizer.pkl"


_movies = None
_similarity = None
_vectorizer = None


def get_movies():

    global _movies

    if _movies is None:

        print("Loading movies...")

        with open(MOVIES_PATH, "rb") as f:

            _movies = pickle.load(f)

    return _movies


def get_similarity():

    global _similarity

    if _similarity is None:

        print("Loading similarity matrix...")

        with open(SIMILARITY_PATH, "rb") as f:

            _similarity = pickle.load(f)

    return _similarity


def get_vectorizer():

    global _vectorizer

    if _vectorizer is None:

        print("Loading TF-IDF vectorizer...")

        with open(TFIDF_PATH, "rb") as f:

            _vectorizer = pickle.load(f)

    return _vectorizer


def movie_exists(title):

    movies = get_movies()

    return movies["title"].str.lower().str.contains(
        title.lower(),
        na=False
    ).any()


def get_movie_index(title):

    movies = get_movies()

    matches = movies[
        movies["title"]
        .str.lower()
        .str.contains(title.lower(), na=False)
    ]

    if matches.empty:
        return None

    return matches.index[0]


def get_movie(index):

    movies = get_movies()

    return movies.iloc[index]


def get_title(index):

    return get_movie(index)["title"]


def normalize(scores):

    scores = np.array(scores)

    minimum = scores.min()

    maximum = scores.max()

    if maximum == minimum:

        return scores

    return (scores - minimum) / (maximum - minimum)