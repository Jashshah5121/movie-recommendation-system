from fastapi import APIRouter
from app.services.similar_movies_service import SimilarMoviesService

router = APIRouter(
    prefix="/movies",
    tags=["Similar Movies"]
)


@router.get("/{movie_id}/similar")
def similar_movies(movie_id: int):
    return SimilarMoviesService.get_similar_movies(movie_id)