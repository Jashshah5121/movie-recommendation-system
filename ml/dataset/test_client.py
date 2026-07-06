from dotenv import load_dotenv
import os

from client import TMDBClient

load_dotenv("../../backend/.env")

TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

print("Token Loaded:", TOKEN is not None)

client = TMDBClient(TOKEN)

movies = client.discover_movies(
    year=2024,
    page=1
)

if movies is None:
    print("Failed to fetch movies.")
    exit()

print("Movies fetched:", len(movies["results"]))

movie = movies["results"][0]

print("Movie:", movie["title"])

details = client.get_movie_details(movie["id"])

print("Runtime:", details["runtime"])

credits = client.get_movie_credits(movie["id"])

print("Lead Actor:", credits["cast"][0]["name"])

keywords = client.get_movie_keywords(movie["id"])

print("Keywords:", keywords["keywords"])

videos = client.get_movie_videos(movie["id"])

print(videos["results"][:2])

details = client.get_movie_details(550)

print(details["title"])

videos = client.get_movie_videos(550)

print(videos)