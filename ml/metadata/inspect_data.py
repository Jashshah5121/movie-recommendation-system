import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ML = ROOT / "ml"

sys.path.append(str(ML))

from recommender.utils import get_movies

movies = get_movies()

print(movies.dtypes)

print("\n")

print(movies.iloc[0].to_dict())