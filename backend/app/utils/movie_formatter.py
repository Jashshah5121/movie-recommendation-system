def split_field(value):
    """
    Convert pipe-separated strings into lists.
    """

    if value is None:
        return []

    value = str(value).strip()

    if value == "":
        return []

    return [item.strip() for item in value.split("|") if item.strip()]


def format_movie(movie: dict):

    return {

        "id": movie["id"],

        "title": movie["title"],

        "overview": movie["overview"],

        "poster": movie["poster"],

        "backdrop": movie["backdrop"],

        "trailer": movie["trailer"],

        "rating": movie["rating"],

        "vote_count": movie["vote_count"],

        "runtime": movie["runtime"],

        "language": movie["language"],

        "release_date": movie["release_date"],

        "year": int(movie["release_date"][:4])
        if movie["release_date"]
        else None,

        "director": movie["director"],

        "tagline": movie["tagline"],

        "genres": split_field(movie["genres"]),

        "keywords": split_field(movie["keywords"]),

        "cast": split_field(movie["movie_cast"]),

        "production_companies": split_field(
            movie["production_companies"]
        ),

        "production_countries": split_field(
            movie["production_countries"]
        ),

        "collection": movie["collection"] or None
    }