import re


class IntentDetector:

    @staticmethod
    def detect(query: str):

        original = query.strip()
        q = original.lower()

        

        if re.search(
            r"(movies?|films?)\s+like|similar\s+to|recommend.*like",
            q
        ):
            return {
                "intent": "SIMILAR_MOVIE",
                "query": original
            }

        

        if re.search(r"\b(19|20)\d{2}\b", q):
            return {
                "intent": "YEAR",
                "query": original
            }

        

        genres = [
            "action",
            "adventure",
            "animation",
            "comedy",
            "crime",
            "drama",
            "fantasy",
            "family",
            "history",
            "horror",
            "music",
            "mystery",
            "romance",
            "science fiction",
            "sci-fi",
            "thriller",
            "war",
            "western",
            "documentary"
        ]

        for genre in genres:
            if genre in q:
                return {
                    "intent": "GENRE",
                    "query": original
                }

        

        languages = [
            "english",
            "hindi",
            "japanese",
            "korean",
            "spanish",
            "french",
            "tamil",
            "telugu"
        ]

        for language in languages:
            if language in q:
                return {
                    "intent": "LANGUAGE",
                    "query": original
                }

       
        person_patterns = [
            r".+\s+movies?$",
            r".+\s+films?$",
            r"movies?\s+of",
            r"films?\s+of",
            r"starring",
            r"directed by"
        ]

        for pattern in person_patterns:
            if re.search(pattern, q):
                return {
                    "intent": "PERSON",
                    "query": original
                }

       

        description_words = [
            "where",
            "about",
            "alive",
            "become",
            "with",
            "whose",
            "who",
            "robot",
            "alien",
            "space",
            "dream",
            "future",
            "time",
            "magic",
            "wizard",
            "superhero",
            "zombie"
        ]

        if any(word in q for word in description_words):
            return {
                "intent": "DESCRIPTION",
                "query": original
            }

        
        return {
            "intent": "EXACT_MOVIE",
            "query": original
        }


detect_intent = IntentDetector.detect