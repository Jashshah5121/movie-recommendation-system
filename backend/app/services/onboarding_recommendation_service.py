from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[3]
ML_DIR = ROOT_DIR / "ml"

if str(ML_DIR) not in sys.path:
    sys.path.append(str(ML_DIR))

from recommender.onboarding_recommender import recommend_from_onboarding


class OnboardingRecommendationService:

    @staticmethod
    def recommend(profile):

        return recommend_from_onboarding(
            selected_movies=profile["favorite_movies"],
            genres=profile["genres"],
            languages=profile["languages"],
            top_k=20,
        )