"""
MovieHub AI
Recommendation Explanation Engine

Generates human-readable explanations for why a movie
was recommended.
"""


class RecommendationExplainer:

    @staticmethod
    def explain(movie, query="", intent="DESCRIPTION", confidence=None):
        """
        Generate an AI explanation for a recommended movie.
        """

        why = []

        # ----------------------------------------------------
        # Metadata reasons
        # ----------------------------------------------------

        if movie.get("why"):
            for item in movie["why"]:
                if item not in why:
                    why.append(item)

        # ----------------------------------------------------
        # Search engines used
        # ----------------------------------------------------

        source_map = {
            "semantic": "Semantic Search",
            "metadata": "Metadata Search",
            "bm25": "Keyword Search",
            "hybrid": "Hybrid Ranking",
            "recommendation": "Recommendation Engine",
            "wishlist": "Wishlist Preference"
        }

        if movie.get("sources"):
            for source in movie["sources"]:
                readable = source_map.get(source.lower(), source)

                if readable not in why:
                    why.append(readable)

        # ----------------------------------------------------
        # Intent specific explanation
        # ----------------------------------------------------

        intent = intent.upper()

        if intent == "EXACT_MOVIE":

            summary = (
                f'Recommended because it is similar to "{query}".'
            )

        elif intent == "SIMILAR_MOVIE":

            summary = (
                f'Found movies similar to "{query}".'
            )

        elif intent == "PERSON":

            summary = (
                f'Found movies associated with "{query}".'
            )

        elif intent == "GENRE":

            summary = (
                f'Matched the "{query}" genre.'
            )

        elif intent == "YEAR":

            summary = (
                f'Matched movies released around {query}.'
            )

        else:

            summary = (
                "Matched your natural language description."
            )

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        if confidence is None:

            score = movie.get("score", 0)

            if isinstance(score, float) and score <= 1:
                confidence = round(score * 100)

            else:
                confidence = int(score)

        confidence = max(0, min(confidence, 100))

        # ----------------------------------------------------
        # Confidence level
        # ----------------------------------------------------

        if confidence >= 90:
            level = "Excellent"

        elif confidence >= 75:
            level = "High"

        elif confidence >= 60:
            level = "Good"

        elif confidence >= 40:
            level = "Medium"

        else:
            level = "Low"

        # ----------------------------------------------------
        # Nice defaults
        # ----------------------------------------------------

        if not why:
            why = ["AI Recommendation"]

        return {

            "summary": summary,

            "confidence": confidence,

            "confidence_level": level,

            "why": why

        }


# ============================================================
# Backward Compatibility
# ============================================================

def generate_explanation(movie, query="", intent="DESCRIPTION"):
    """
    Legacy wrapper for older modules.
    """

    return RecommendationExplainer.explain(
        movie=movie,
        query=query,
        intent=intent
    )