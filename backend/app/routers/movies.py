from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.services.movie_service import MovieService
from app.services.tmdb_service import TMDBService

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/trending")
def trending_movies():
    return TMDBService.trending()


@router.get("/popular")
def popular_movies():
    return TMDBService.popular()


@router.get("/top-rated")
def top_rated_movies():
    return TMDBService.top_rated()


@router.get("/upcoming")
def upcoming_movies():
    return TMDBService.upcoming()


@router.get("/search")
def search_movies(
    query: str = Query(..., min_length=1)
):
    return TMDBService.search(query)


@router.get("/onboarding")
def onboarding_movies(

    language: List[str] = Query(default=[]),

    genres: List[str] = Query(default=[])

):

    return MovieService.get_onboarding_movies(

    languages=language,

    genres=genres

)


@router.get("/{movie_id}")
def movie_details(movie_id: int):

    movie = MovieService.get_movie(movie_id)

    if movie is None:

        raise HTTPException(

            status_code=404,

            detail="Movie not found"

        )

    return movie


@router.get("/{movie_id}/recommendations")
def movie_recommendations(movie_id: int):

    return TMDBService.recommendations(movie_id)