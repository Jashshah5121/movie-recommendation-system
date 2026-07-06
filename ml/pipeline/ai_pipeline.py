from resolver.query_resolver import QueryResolver

from recommender.fuzzy_search import resolve_movie
from recommender.recommendation_engine import recommend

from recommender.semantic_engine import semantic_search
from recommender.bm25_engine import bm25_search
from recommender.rrf import reciprocal_rank_fusion

from metadata.metadata_search import MetadataSearch
from recommender.explain import RecommendationExplainer


class AIPipeline:

    @staticmethod
    def add_explanations(results, query, intent):

            if not results:
                return []

            for rank, movie in enumerate(results):

                # Confidence based on final rank
                confidence = max(70, 98 - rank * 3)

                movie["score"] = confidence

                movie["explanation"] = RecommendationExplainer.explain(
                    movie,
                    query=query,
                    intent=intent,
                    confidence=confidence
)
                
                
                

            return results

    @staticmethod
    def search(query: str, top_k=10):

        resolved = QueryResolver.resolve(query)

        intent = resolved["intent"]

        # =====================================================
        # EXACT MOVIE
        # =====================================================

        if intent == "EXACT_MOVIE":

            movie = resolve_movie(
                resolved["entity"]
            )

            if movie is None:

                return {
                    "intent": intent,
                    "results": []
                }

            recommendations = recommend(
                movie["title"],
                top_k=top_k
            )

            recommendations = AIPipeline.add_explanations(
                recommendations,
                query,
                intent
            )

            return {

                "intent": intent,

                "resolved_movie": movie,

                "results": recommendations

            }

        # =====================================================
        # SIMILAR MOVIE
        # =====================================================

        if intent == "SIMILAR_MOVIE":

            movie = resolve_movie(
                resolved["entity"]
            )

            if movie is None:

                return {

                    "intent": intent,

                    "results": []

                }

            recommendations = recommend(
                movie["title"],
                top_k=top_k
            )

            recommendations = AIPipeline.add_explanations(
                recommendations,
                query,
                intent
            )

            return {

                "intent": intent,

                "resolved_movie": movie,

                "results": recommendations

            }

        # =====================================================
        # PERSON
        # =====================================================

        if intent == "PERSON":

            results = MetadataSearch.search(
                resolved["entity"],
                top_k
            )

            results = AIPipeline.add_explanations(
                results,
                query,
                intent
            )

            return {

                "intent": intent,

                "entity": resolved["entity"],

                "results": results

            }

        # =====================================================
        # GENRE
        # =====================================================

        if intent == "GENRE":

            results = MetadataSearch.search(
                resolved["entity"],
                top_k
            )

            results = AIPipeline.add_explanations(
                results,
                query,
                intent
            )

            return {

                "intent": intent,

                "results": results

            }

        # =====================================================
        # YEAR
        # =====================================================

        if intent == "YEAR":

            results = MetadataSearch.search(
                resolved["entity"],
                top_k
            )

            results = AIPipeline.add_explanations(
                results,
                query,
                intent
            )

            return {

                "intent": intent,

                "results": results

            }

        # =====================================================
        # LANGUAGE
        # =====================================================

        if intent == "LANGUAGE":

            results = MetadataSearch.search(
                resolved["entity"],
                top_k
            )

            results = AIPipeline.add_explanations(
                results,
                query,
                intent
            )

            return {

                "intent": intent,

                "results": results

            }

        # =====================================================
        # DESCRIPTION (Semantic + BM25 + RRF)
        # =====================================================

        semantic = semantic_search(
            resolved["entity"],
            top_k=20
        )

        bm25 = bm25_search(
            resolved["entity"],
            top_k=20
        )

        fused = reciprocal_rank_fusion(
            semantic,
            bm25
        )

        results = fused[:top_k]

        results = AIPipeline.add_explanations(
            results,
            query,
            intent
        )

        return {

            "intent": "DESCRIPTION",

            "results": results

        }