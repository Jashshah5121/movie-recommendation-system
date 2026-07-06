import time
from urllib import response
import requests


class TMDBClient:

    def __init__(self, token):

        self.base_url = "https://api.themoviedb.org/3"

        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        })

    # -----------------------------------------
    # Internal Request Method
    # -----------------------------------------

    def _get(self, endpoint, params=None):

        url = f"{self.base_url}{endpoint}"

        for attempt in range(5):

            try:

                response = self.session.get(
                    url,
                    params=params,
                    timeout=30
                )

                print("\n--------------------------------")
                print("URL:", response.url)
                print("Status:", response.status_code)

                response.raise_for_status()

                data = response.json()

                print("Keys:", data.keys())

                return data

            except requests.exceptions.RequestException as e:

                print(
                    f"[Retry {attempt + 1}/5] {endpoint}"
                )

                print(e)

                time.sleep(2)

        return None

    # -----------------------------------------
    # Discover Movies
    # -----------------------------------------

    def discover_movies(
        self,
        year,
        page=1
    ):

        return self._get(

            "/discover/movie",

            params={

                "primary_release_year": year,

                "sort_by": "popularity.desc",

                "page": page,

                "include_adult": False

            }

        )

    # -----------------------------------------
    # Movie Details
    # -----------------------------------------

    def get_movie_details(
        self,
        movie_id
    ):

        return self._get(

            f"/movie/{movie_id}"

        )

    # -----------------------------------------
    # Credits
    # -----------------------------------------

    def get_movie_credits(
        self,
        movie_id
    ):

        return self._get(

            f"/movie/{movie_id}/credits"

        )

    # -----------------------------------------
    # Keywords
    # -----------------------------------------

    def get_movie_keywords(
        self,
        movie_id
    ):

        return self._get(

            f"/movie/{movie_id}/keywords"

        )
    
    def get_movie_videos(self, movie_id):
        return self._get(
        f"/movie/{movie_id}/videos"
    )