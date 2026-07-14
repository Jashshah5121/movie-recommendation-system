import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { ProfileContext } from "../../context/ProfileContext";

import {
    getOnboardingMovies,
    getOnboardingRecommendations
} from "../../services/movieService";

import "./Onboarding.css";

export default function FavoriteMovies() {

    const navigate = useNavigate();

    const {
        profile,
        updateLikedMovies,
        updateRecommendedMovies,
        completeOnboarding
    } = useContext(ProfileContext);

    const [movies, setMovies] = useState([]);
    const [selected, setSelected] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        if (
            profile.languages.length === 0 ||
            profile.genres.length === 0
        ) return;

        loadMovies();

    }, [profile]);

    async function loadMovies() {

        try {

            const data = await getOnboardingMovies(
                profile.languages,
                profile.genres
            );

            setMovies(data);

        } catch (err) {

            console.error(err);

        } finally {

            setLoading(false);

        }

    }

    function toggleMovie(id) {

        if (selected.includes(id)) {

            setSelected(selected.filter(movie => movie !== id));

            return;

        }

        setSelected([...selected, id]);

    }

    async function continueNext() {

        if (selected.length < 3) return;

        updateLikedMovies(selected);

        try {

            const response = await getOnboardingRecommendations({
                genres: profile.genres,
                languages: profile.languages,
                favorite_movies: selected
            });

            updateRecommendedMovies(response.results);

        } catch (err) {

            console.error(err);

        }

        completeOnboarding();

        navigate("/");

    }

    if (loading) {

        return (
            <div className="onboarding-card">
                <h1>Loading Movies...</h1>
            </div>
        );

    }

    return (

        <div className="onboarding-card has-sticky-footer">

            <div className="step-text">
                Step 3 of 4
            </div>

            <h1>
                Pick Movies You Love
            </h1>

            <p>
                Select at least 3 movies you've enjoyed.
            </p>

            <div className="selection-count">
                Selected {selected.length} / 3 Minimum
            </div>

            <div className="movie-grid">

                {
                    movies.map(movie => {

                        const isSelected = selected.includes(movie.id);

                        return (

                            <div
                                key={movie.id}
                                className={`movie-card ${isSelected ? "selected" : ""}`}
                                onClick={() => toggleMovie(movie.id)}
                            >

                                <img
                                    src={
                                        movie.poster
                                            ? `https://image.tmdb.org/t/p/w500${movie.poster}`
                                            : "https://placehold.co/500x750?text=No+Poster"
                                    }
                                    alt={movie.title}
                                />

                                <div className="movie-title">
                                    {movie.title}
                                </div>

                                {
                                    isSelected && (
                                        <div className="selected-badge">
                                            ✔
                                        </div>
                                    )
                                }

                            </div>

                        );

                    })
                }

            </div>

            <div className="sticky-footer">

                <div className="sticky-footer-inner">

                    <span className="sticky-footer-count">
                        Selected {selected.length} / 3 Minimum
                    </span>

                    <button
                        className="continue-btn"
                        disabled={selected.length < 3}
                        onClick={continueNext}
                    >
                        Finish →
                    </button>

                </div>

            </div>

        </div>

    );

}

