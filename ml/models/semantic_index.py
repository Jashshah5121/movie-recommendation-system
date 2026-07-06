import pickle
import numpy as np

from pathlib import Path

from sklearn.neighbors import NearestNeighbors


BASE_DIR = Path(__file__).parent.parent

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

EMBEDDINGS_FILE = EMBEDDINGS_DIR / "sentence_embeddings.npy"

INDEX_FILE = EMBEDDINGS_DIR / "semantic_index.pkl"


print("=" * 60)
print("Loading embeddings...")

embeddings = np.load(EMBEDDINGS_FILE)

print("Embeddings:", embeddings.shape)

print()
print("=" * 60)
print("Building NearestNeighbors Index...")

nn = NearestNeighbors(
    n_neighbors=20,
    metric="cosine",
    algorithm="brute"
)

nn.fit(embeddings)

print()
print("=" * 60)
print("Saving index...")

with open(INDEX_FILE, "wb") as f:
    pickle.dump(nn, f)

print("semantic_index.pkl created successfully!")

print("=" * 60)