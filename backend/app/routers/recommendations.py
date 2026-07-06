from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.recommendation_service import RecommendationService
from pydantic import BaseModel
from app.services.onboarding_recommendation_service import (
    OnboardingRecommendationService,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# -----------------------------------------
# Request Model
# -----------------------------------------
class OnboardingRequest(BaseModel):
    genres: list[str]
    languages: list[str]
    favorite_movies: list[int]

class WishlistRequest(BaseModel):

    movie_ids: list[int]


# -----------------------------------------
# Single Movie Recommendations
# -----------------------------------------

@router.get("/{movie_id}")
def recommendations(movie_id: int):

    result = RecommendationService.recommend(movie_id)

    if result is None:

        raise HTTPException(

            status_code=404,

            detail="Movie not found"

        )

    return result


# -----------------------------------------
# Wishlist Recommendations
# -----------------------------------------

@router.post("/wishlist")
def wishlist_recommendations(request: WishlistRequest):

    return RecommendationService.recommend_from_wishlist(
        request.movie_ids
    )

@router.post("/onboarding")
def onboarding_recommendations(request: OnboardingRequest):

    results = OnboardingRecommendationService.recommend(
        request.model_dump()
    )

    return {
        "results": results
    }