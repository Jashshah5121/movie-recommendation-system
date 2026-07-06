import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import TrailerModal from "../components/TrailerModal/TrailerModal";
import MovieRow from "../components/MovieRow/MovieRow";
import { Heart } from "lucide-react";
import useWishlist from "../hooks/useWishlist";
import {
    getMovieDetails,
    getRecommendations
} from "../services/movieService";

import "./MovieDetails.css";

const IMAGE = "https://image.tmdb.org/t/p/original";
const POSTER = "https://image.tmdb.org/t/p/w500";

function MovieDetails() {

    const { id } = useParams();

    const [movie, setMovie] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [showTrailer, setShowTrailer] = useState(false);
    const {
    toggleWishlist,
    isWishlisted
    } = useWishlist();

    const wishlisted = movie ? isWishlisted(movie.id) : false;
    useEffect(() => {

        async function loadMovie() {

            try {

                const details = await getMovieDetails(id);
                setMovie(details);

                const recs = await getRecommendations(id);
                setRecommendations(recs);

            }

            catch (err) {

                console.error(err);

            }

        }

        loadMovie();

    }, [id]);

    if (!movie) {

        return (

            <div className="loading">

                Loading...

            </div>

        );

    }

    return (

        <div className="movie-page">

            <div
                className="movie-backdrop"
                style={{
                    backgroundImage: `url(${IMAGE}${movie.backdrop})`
                }}
            >
                <div className="backdrop-overlay"></div>
            </div>

            <div className="movie-content">

                <img
                    className="movie-poster"
                    src={POSTER + movie.poster}
                    alt={movie.title}
                />

                <div className="movie-info">

                    <h1>{movie.title}</h1>

                    {movie.tagline && (

                        <p className="tagline">

                            {movie.tagline}

                        </p>

                    )}

                    <div className="movie-meta">

                        <span>⭐ {movie.rating}</span>

                        <span>{movie.release_date}</span>

                        <span>{movie.runtime} min</span>

                        <span>{movie.language.toUpperCase()}</span>

                    </div>

                    <p className="overview">

                        {movie.overview}

                    </p>

                    <div className="chips">

                        {movie.genres?.map((genre) => (

                            <span
                                className="chip"
                                key={genre}
                            >
                                {genre}
                            </span>

                        ))}

                    </div>

                    <h3>Director</h3>

                    <p>{movie.director}</p>

                    <h3>Top Cast</h3>

                    <div className="chips">

                        {movie.cast?.map((actor) => (

                            <span
                                className="chip"
                                key={actor}
                            >
                                {actor}
                            </span>

                        ))}

                    </div>
                    <div className="movie-actions">

                        <button
                            className="wishlist-detail-btn"
                            onClick={() => toggleWishlist(movie)}
                        >

                            <Heart
                                size={20}
                                fill={wishlisted ? "#e50914" : "none"}
                                color={wishlisted ? "#e50914" : "white"}
                            />

                            {wishlisted
                                ? "Remove from Wishlist"
                                : "Add to Wishlist"}

                        </button>

                        {movie.trailer && (

                            <button
                                className="watch-btn"
                                onClick={() => setShowTrailer(true)}
                            >

                                ▶ Watch Trailer

                            </button>

                        )}

                    </div>

                </div>

            </div>

            <MovieRow
                title="🎬 You May Also Like"
                movies={recommendations}
            />

            {showTrailer && (

                <TrailerModal

                    trailerKey={movie.trailer}

                    onClose={() => setShowTrailer(false)}

                />

            )}

        </div>

    );

}

export default MovieDetails;