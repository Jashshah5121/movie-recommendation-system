import time
import requests

from app.core.config import settings

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

HEADERS = {
    "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}",
    "accept": "application/json",
}

# Reuse one HTTP connection for all requests
session = requests.Session()
session.headers.update(HEADERS)


class TMDBService:

    @staticmethod
    def format_movies(results):
        movies = []

        for movie in results:
            movies.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "poster": (
                    f"{IMAGE_BASE}{movie.get('poster_path')}"
                    if movie.get("poster_path")
                    else None
                ),
                "backdrop": (
                    f"{IMAGE_BASE}{movie.get('backdrop_path')}"
                    if movie.get("backdrop_path")
                    else None
                ),
                "rating": movie.get("vote_average"),
                "release_date": movie.get("release_date"),
            })

        return movies

    @staticmethod
    def get(endpoint, params=None):

        if params is None:
            params = {}

        url = f"{BASE_URL}/{endpoint}"

        # Retry up to 3 times if TMDB temporarily disconnects
        for attempt in range(3):

            try:

                print(f"Calling: {url}")

                response = session.get(
                    url,
                    params=params,
                    timeout=20,
                )

                response.raise_for_status()

                return response.json()

            except requests.exceptions.RequestException as e:

                print(f"Attempt {attempt + 1} failed: {e}")

                if attempt == 2:
                    raise

                time.sleep(1)

    @staticmethod
    def trending():
        data = TMDBService.get("trending/movie/week")
        return TMDBService.format_movies(data["results"])

    @staticmethod
    def popular():
        data = TMDBService.get("movie/popular")
        return TMDBService.format_movies(data["results"])

    @staticmethod
    def top_rated():
        data = TMDBService.get("movie/top_rated")
        return TMDBService.format_movies(data["results"])

    @staticmethod
    def upcoming():
        data = TMDBService.get("movie/upcoming")
        return TMDBService.format_movies(data["results"])

    @staticmethod
    def movie(movie_id):
        return TMDBService.get(f"movie/{movie_id}")

    @staticmethod
    def search(query):
        data = TMDBService.get(
            "search/movie",
            {"query": query},
        )
        return TMDBService.format_movies(data["results"])

    @staticmethod
    def recommendations(movie_id):
        data = TMDBService.get(
            f"movie/{movie_id}/recommendations"
        )
        return TMDBService.format_movies(data["results"])