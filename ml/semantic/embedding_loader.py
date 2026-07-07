import pickle
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer

from recommender.utils import get_movies



BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

INDEX_FILE = EMBEDDINGS_DIR / "semantic_index.pkl"

EMBEDDINGS_FILE = EMBEDDINGS_DIR / "sentence_embeddings.npy"


class EmbeddingLoader:

    _loaded = False

    model = None

    index = None

    embeddings = None

    movies = None

    @classmethod
    def load(cls):

        if cls._loaded:

            return

        print("=" * 60)
        print("Loading Semantic AI Engine...")
        print("=" * 60)

        cls.movies = get_movies()

        cls.embeddings = np.load(
            EMBEDDINGS_FILE
        )

        with open(INDEX_FILE, "rb") as f:

            cls.index = pickle.load(f)

        cls.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        cls._loaded = True

        print(f"Movies Loaded      : {len(cls.movies)}")
        print(f"Embeddings Loaded : {cls.embeddings.shape}")
        print("Semantic Engine Ready!")
        print("=" * 60)