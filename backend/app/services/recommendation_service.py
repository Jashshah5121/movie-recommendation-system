from pathlib import Path
import sys

# -------------------------------------------------------
# Make the ml folder importable
# -------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]
ML_DIR = ROOT_DIR / "ml"

if str(ML_DIR) not in sys.path:
    sys.path.append(str(ML_DIR))

from recommender.search_router import search
from recommender.recommendation_engine import recommend
from recommender.wishlist_engine import recommend_from_wishlist
from recommender.utils import get_movies


class RecommendationService:

    @staticmethod
    def search(query: str):
        return search(query)

    @staticmethod
    def recommend(movie_id: int, top_k: int = 10):

        movies = get_movies()

        movie = movies[movies["id"] == movie_id]

        if movie.empty:
            return None

        title = movie.iloc[0]["title"]

        recommendations = recommend(title, top_k)

        return {
            "movie": {
                "id": int(movie.iloc[0]["id"]),
                "title": title,
            },
            "recommendations": recommendations,
        }

    @staticmethod
    def recommend_from_wishlist(movie_ids, top_k=20):
        return recommend_from_wishlist(movie_ids, top_k)