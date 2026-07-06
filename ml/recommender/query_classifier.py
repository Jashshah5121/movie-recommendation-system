import re


QUESTION_WORDS = {
    "what",
    "which",
    "who",
    "where",
    "when",
    "why",
    "how",
    "movie",
    "movies",
    "film",
    "films",
    "recommend",
    "recommendation",
    "similar",
    "like",
    "about"
}


COMMON_CONNECTORS = {
    "inside",
    "through",
    "between",
    "without",
    "with",
    "into",
    "from",
    "because",
    "while",
    "after",
    "before",
    "during",
    "another",
    "becomes",
    "become"
}


def clean_query(query):

    query = query.lower()

    query = re.sub(r"[^a-z0-9\s]", " ", query)

    query = " ".join(query.split())

    return query


def classify_query(query):

    query = clean_query(query)

    words = query.split()

    if not words:
        return "unknown"

    # Question-like queries
    if any(word in QUESTION_WORDS for word in words):
        return {
                "type": "natural_language",
                "confidence": 0.95
}

    # Longer descriptive queries
    if len(words) >= 5:
        return {
                "type": "natural_language",
                "confidence": 0.95
}

    # Descriptive connector words
    if any(word in COMMON_CONNECTORS for word in words):
       return {
            "type": "natural_language",
            "confidence": 0.95
}

    # Otherwise assume title
    return {
        "type": "movie_title",
        "confidence": 0.90
    }