from fastapi import APIRouter, HTTPException

from app.services.movie_service import MovieService

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/{movie_id}")
def get_movie(movie_id: int):

    movie = MovieService.get_movie(movie_id)

    if movie is None:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie