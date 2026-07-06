import re

from intent.intent_detector import detect_intent


class QueryResolver:

    @staticmethod
    def resolve(query: str):

        detected = detect_intent(query)

        intent = detected["intent"]
        text = detected["query"]

        # -------------------------
        # Similar Movie
        # -------------------------

        if intent == "SIMILAR_MOVIE":

            movie = re.sub(
                r"(movies?|films?)\s+like|similar\s+to|recommend.*like",
                "",
                text,
                flags=re.IGNORECASE
            ).strip()

            return {

                "intent": intent,

                "entity": movie

            }

        # -------------------------
        # Person
        # -------------------------

        if intent == "PERSON":

            entity = re.sub(
                r"movies?|films?|starring|directed by|of",
                "",
                text,
                flags=re.IGNORECASE
            ).strip()

            return {

                "intent": intent,

                "entity": entity

            }

        # -------------------------
        # Others
        # -------------------------

        return {

            "intent": intent,

            "entity": text

        }