from enum import Enum

from fastapi import APIRouter, Query

from app.services.discover_service import DiscoverService


class SortType(str, Enum):
    popularity = "popularity"
    rating = "rating"
    newest = "newest"
    oldest = "oldest"


router = APIRouter(
    prefix="/discover",
    tags=["Discover"]
)


@router.get("")
def discover(

    genre: str | None = Query(
        None,
        title="Genre",
        description="Comma separated genres. Example: Action,Adventure"
    ),

    language: str | None = Query(
        None,
        title="Language",
        description="Language code (en, hi, ja, fr...)"
    ),

    from_year: int | None = Query(
        None,
        ge=1900,
        le=2100,
        title="From Year",
        description="Show movies released after this year"
    ),

    to_year: int | None = Query(
        None,
        ge=1900,
        le=2100,
        title="To Year",
        description="Show movies released before this year"
    ),

    min_rating: float | None = Query(
        None,
        ge=0,
        le=10,
        title="Minimum Rating",
        description="Minimum TMDB rating"
    ),

    max_runtime: int | None = Query(
        None,
        ge=1,
        le=500,
        title="Maximum Runtime",
        description="Maximum runtime in minutes"
    ),

    sort: SortType = Query(
        SortType.popularity,
        title="Sort By"
    ),

    page: int = Query(
        1,
        ge=1,
        title="Page Number"
    ),

    limit: int = Query(
        20,
        ge=1,
        le=100,
        title="Results Per Page"
    )

):

    return DiscoverService.discover(

        genre=genre,

        language=language,

        from_year=from_year,

        to_year=to_year,

        min_rating=min_rating,

        max_runtime=max_runtime,

        sort=sort.value,

        page=page,

        limit=limit

    )