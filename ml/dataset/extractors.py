def safe_join(items):
    """
    Convert a list into a pipe separated string.
    """

    if not items:
        return ""

    return "|".join(items)


def extract_movie_data(
    movie,
    details,
    credits,
    keywords,
    videos
):



    director = ""

    for crew in credits.get("crew", []):

        if crew.get("job") == "Director":
            director = crew.get("name", "")
            break



    movie_cast = []

    for actor in credits.get("cast", [])[:3]:
        movie_cast.append(actor.get("name", ""))


    keyword_list = []

    for keyword in keywords.get("keywords", []):
        keyword_list.append(keyword.get("name", ""))

    genres = []

    for genre in details.get("genres", []):
        genres.append(genre.get("name", ""))


    companies = []

    for company in details.get("production_companies", []):
        companies.append(company.get("name", ""))



    countries = []

    for country in details.get("production_countries", []):
        countries.append(country.get("name", ""))



    trailer = ""

    for video in videos.get("results", []):

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):

            trailer = video.get("key", "")
            break



    collection = ""

    if details.get("belongs_to_collection"):
        collection = details["belongs_to_collection"].get("name", "")



    return {

        "id": movie["id"],

        "title": movie.get("title", ""),

        "overview": movie.get("overview", ""),

        "genres": safe_join(genres),

        "keywords": safe_join(keyword_list),

        "movie_cast": safe_join(movie_cast),

        "director": director,

        "language": movie.get("original_language", ""),

        "release_date": movie.get("release_date", ""),

        "runtime": details.get("runtime", 0),

        "rating": movie.get("vote_average", 0),

        "vote_count": movie.get("vote_count", 0),

        "popularity": movie.get("popularity", 0),

        "poster": movie.get("poster_path", ""),

        "backdrop": movie.get("backdrop_path", ""),

        "tagline": details.get("tagline", ""),

        "collection": collection,

        "production_companies": safe_join(companies),

        "production_countries": safe_join(countries),

        "adult": int(movie.get("adult", False)),

        "trailer": trailer

    }