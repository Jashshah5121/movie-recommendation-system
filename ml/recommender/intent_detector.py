import re

GENRES = {
    "action",
    "adventure",
    "animation",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "family",
    "fantasy",
    "history",
    "horror",
    "music",
    "mystery",
    "romance",
    "science fiction",
    "sci-fi",
    "thriller",
    "war",
    "western"
}

MOODS = {
    "funny",
    "sad",
    "happy",
    "romantic",
    "dark",
    "scary",
    "mind bending",
    "mind-bending",
    "emotional",
    "feel good",
    "family"
}


def normalize(query: str):

    query = query.lower()

    query = re.sub(r"\s+", " ", query)

    return query.strip()


def detect_intent(query: str):

    q = normalize(query)

    # Similar movie

    if "like " in q or q.startswith("movies like"):

        return {
            "intent": "SIMILAR_MOVIE",
            "query": query
        }

    # Director

    if "director" in q:

        return {
            "intent": "DIRECTOR",
            "query": query
        }

    # Actor

    if "actor" in q or "starring" in q:

        return {
            "intent": "ACTOR",
            "query": query
        }

    # Genre

    for genre in GENRES:

        if genre in q:

            return {

                "intent": "GENRE",

                "query": query

            }

    # Mood

    for mood in MOODS:

        if mood in q:

            return {

                "intent": "MOOD",

                "query": query

            }

    # Description Search

    if len(q.split()) >= 4:

        return {

            "intent": "DESCRIPTION",

            "query": query

        }

    # Default

    return {

        "intent": "EXACT_MOVIE",

        "query": query

    }