import "./MovieCard.css";

import { Link } from "react-router-dom";

import {
    Star,
    Heart,
    Sparkles
} from "lucide-react";

import useWishlist from "../../hooks/useWishlist";

const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

function MovieCard({ movie }) {

    const {
        toggleWishlist,
        isWishlisted
    } = useWishlist();

    const year = movie.release_date
        ? movie.release_date.substring(0, 4)
        : movie.year;

    const wishlisted = isWishlisted(movie.id);

    return (

        <Link
            to={`/movie/${movie.id}`}
            className="movie-card-link"
        >

            <div className="movie-card">

                <div className="poster-container">

                    <img
                        src={`${IMAGE_BASE_URL}${movie.poster}`}
                        alt={movie.title}
                        className="movie-poster"
                    />

                    <button

                        className="wishlist-btn"

                        onClick={(e) => {

                            e.preventDefault();
                            e.stopPropagation();

                            toggleWishlist(movie);

                        }}

                    >

                        <Heart

                            size={22}

                            fill={wishlisted ? "#e50914" : "none"}

                            color={wishlisted ? "#e50914" : "white"}

                        />

                    </button>

                    <div className="movie-overlay">

                        <div className="rating">

                            <Star
                                size={16}
                                fill="gold"
                            />

                            {movie.rating?.toFixed(1)}

                        </div>

                    </div>

                </div>

                <div className="movie-info">

                    <h3>{movie.title}</h3>

                    <p>{year}</p>

                    {movie.match && (

                        <div className="match-score">

                            <Sparkles size={15} />

                            {movie.match} Match

                        </div>

                    )}

                    {movie.why?.length > 0 && (

                        <div className="why-section">

                            {movie.why.slice(0,3).map((reason,index)=>(

                                <span
                                    key={index}
                                    className="reason-chip"
                                >

                                    {reason}

                                </span>

                            ))}

                        </div>

                    )}

                </div>

            </div>

        </Link>

    );

}

export default MovieCard;