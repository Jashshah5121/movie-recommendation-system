from app.services.tmdb_service import TMDBService
from ml.pipeline.ai_pipeline import AIPipeline


class SmartSearchService:

    @staticmethod
    def search(query: str):

        query = query.strip()

        if not query:
            return {
                "mode": "empty",
                "results": []
            }

        # -------------------------------------------------
        # Simple movie title search
        # -------------------------------------------------

        simple = TMDBService.search(query)

        if simple:

            first_movie = simple[0]

            recommendations = TMDBService.recommendations(
                first_movie["id"]
            )

            return {
                "mode": "movie",
                "movie": first_movie,
                "results": recommendations
            }

        # -------------------------------------------------
        # AI Search
        # -------------------------------------------------

        ai_results = AIPipeline.search(
            query=query,
            top_k=12
        )

        return {
            "mode": "ai",
            "results": ai_results
        }