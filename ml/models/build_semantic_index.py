import pickle
import numpy as np

from pathlib import Path
from sklearn.neighbors import NearestNeighbors

BASE_DIR = Path(__file__).parent.parent

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

EMBEDDINGS_FILE = EMBEDDINGS_DIR / "sentence_embeddings.npy"

INDEX_FILE = EMBEDDINGS_DIR / "semantic_index.pkl"

print("=" * 60)
print("Loading sentence embeddings...")

embeddings = np.load(EMBEDDINGS_FILE)

print("Embeddings Shape :", embeddings.shape)

print()
print("=" * 60)
print("Building NearestNeighbors Index...")

index = NearestNeighbors(
    n_neighbors=20,
    metric="cosine",
    algorithm="brute"
)

index.fit(embeddings)

print("Index built successfully!")

print()
print("=" * 60)
print("Saving semantic index...")

with open(INDEX_FILE, "wb") as f:
    pickle.dump(index, f)

print("Saved :", INDEX_FILE)

print("=" * 60)
print("Done!")