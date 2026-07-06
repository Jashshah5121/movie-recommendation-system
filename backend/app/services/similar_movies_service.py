import sys
from pathlib import Path

# ----------------------------
# Add ml folder to Python path
# ----------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]
ML_DIR = ROOT_DIR / "ml"

if str(ML_DIR) not in sys.path:
    sys.path.append(str(ML_DIR))

from recommender.recommendation_engine import recommend
from recommender.utils import get_movies


class SimilarMoviesService:

    @staticmethod
    def get_similar_movies(movie_id: int):

        movies = get_movies()

        movie = movies[movies["id"] == movie_id]

        if movie.empty:
            return {
                "results": []
            }

        title = movie.iloc[0]["title"]

        recommendations = recommend(
            title,
            top_k=15
        )

        return {
            "results": recommendations
        }