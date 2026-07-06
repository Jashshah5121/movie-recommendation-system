from pathlib import Path
import sys

# -------------------------------------------------------
# Make the ml folder importable
# -------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]
ML_DIR = ROOT_DIR / "ml"

if str(ML_DIR) not in sys.path:
    sys.path.append(str(ML_DIR))

from recommender.onboarding_movies import ONBOARDING_MOVIES
from app.services.movie_service import MovieService


class OnboardingService:

    @staticmethod
    def get_movies():

        movies = []

        for movie_id in ONBOARDING_MOVIES:

            movie = MovieService.get_movie(movie_id)

            if movie:
                movies.append(movie)

        return movies