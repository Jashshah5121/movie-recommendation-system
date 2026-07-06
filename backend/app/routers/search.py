from fastapi import APIRouter
from app.services.recommendation_service import RecommendationService
from app.services.movie_service import MovieService
router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def search_movies(query: str):

    return RecommendationService.search(query)

@router.get("/autocomplete")
def autocomplete(query: str):
    return MovieService.autocomplete(query)