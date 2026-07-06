import { useState } from "react";
import "./AIRecommend.css";

import SearchBar from "../../SearchBar/SearchBar";
import SearchMovieHero from "../../components/SearchMovieHero/SearchMovieHero";
import RecommendationCard from "../../components/RecommendationCard/RecommendationCard";
import Loading from "../../components/Loading/Loading";

import { smartSearch } from "../../services/movieService";

function AIRecommend() {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [mode, setMode] = useState("");
    const [heroMovie, setHeroMovie] = useState(null);
    const [movies, setMovies] = useState([]);
    const [summary, setSummary] = useState(null);
    const [intent, setIntent] = useState("");
    const [searchedMovie, setSearchedMovie] = useState("");

    const handleSearch = async () => {
        if (!query.trim()) return;

        try {
            setLoading(true);
            setMovies([]);
            setHeroMovie(null);
            setSummary(null);
            setIntent("");

            const response = await smartSearch(query);

            if (response.mode === "movie") {
                setMode("movie");
                setHeroMovie(response.movie);
                setMovies(response.results || []);
                setSearchedMovie(response.movie.title);
                return;
            }

            const ai = response.results;
            setMode("ai");
            setIntent(ai.intent || "");
            setSummary(ai.ai_summary || null);
            setMovies(ai.results || []);
            setSearchedMovie(
                ai.entity ||
                ai.query ||
                query
            );
        } catch (err) {
            console.log(err);
            setMovies([]);
            setHeroMovie(null);
            setSummary(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="ai-page">
            <SearchBar
                query={query}
                setQuery={setQuery}
                onSearch={handleSearch}
                loading={loading}
            />

            {loading && (
                <div className="loading-section">
                    <Loading />
                    <p className="loading-text">
                        🧠 Searching MovieHub...
                    </p>
                    <p className="loading-sub">
                        Searching TMDB...
                        <br />
                        Understanding your request...
                        <br />
                        Finding the best recommendations...
                    </p>
                </div>
            )}

            {!loading && mode === "movie" && heroMovie && (
                <SearchMovieHero
                    movie={heroMovie}
                />
            )}

            {!loading && mode === "ai" && intent && (
                <p className="intent">
                    Intent:
                    <strong> {intent}</strong>
                </p>
            )}

            {!loading && mode === "ai" && summary && (
                <div className="ai-summary">
                    <div className="ai-summary-icon">
                        🧠
                    </div>
                    <div className="ai-summary-content">
                        <h2>
                            AI understood your request
                        </h2>
                        <h3>
                            {summary.title}
                        </h3>
                        <p>
                            {summary.description}
                        </p>
                    </div>
                </div>
            )}

            {!loading && movies.length > 0 && (
                <>
                    <h2 className="results-title">
                        {mode === "movie"
                            ? `Because you searched "${searchedMovie}"`
                            : `AI Recommendations`
                        }
                    </h2>

                    <div className="recommendation-grid">
                        {movies.map((movie) => (
                            <RecommendationCard
                                key={movie.id}
                                movie={movie}
                            />
                        ))}
                    </div>
                </>
            )}

            {!loading && searchedMovie && movies.length === 0 && (
                <div className="empty-results">
                    <h2>
                        😔 Nothing Found
                    </h2>
                    <p>
                        We couldn't find any matching movies.
                    </p>
                    <p>
                        Try another movie title,
                        actor,
                        director,
                        genre,
                        or describe the movie differently.
                    </p>
                </div>
            )}

            {!loading && (
                <div className="powered">
                    Powered by
                    <b> TMDB </b>
                    +
                    <b> MovieHub AI </b>
                </div>
            )}
        </div>
    );
}

export default AIRecommend;