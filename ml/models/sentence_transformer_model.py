import pickle
import numpy as np
import pandas as pd

from pathlib import Path
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).parent.parent

DATASET = BASE_DIR / "preprocessing" / "combined_features.csv"

EMBEDDINGS_DIR = BASE_DIR / "embeddings"

MODEL_NAME = "all-MiniLM-L6-v2"

OUTPUT = EMBEDDINGS_DIR / "sentence_embeddings.npy"


print("=" * 60)
print("Loading Dataset...")

movies = pd.read_csv(DATASET)

movies["semantic_features"] = movies["semantic_features"].fillna("")
print(f"{len(movies)} movies loaded")

print()
print("=" * 60)
print("Loading Sentence Transformer...")

model = SentenceTransformer(MODEL_NAME)

print("Model Loaded")

print()
print("=" * 60)
print("Generating Embeddings...")

embeddings = model.encode(

    movies["semantic_features"].tolist(),

    batch_size=64,

    show_progress_bar=True,

    convert_to_numpy=True,

    normalize_embeddings=True

)

print()
print("=" * 60)
print("Saving Embeddings...")

np.save(

    OUTPUT,

    embeddings

)

print()

print("Embeddings Shape :", embeddings.shape)

print()

print("Saved :", OUTPUT)

print("=" * 60)