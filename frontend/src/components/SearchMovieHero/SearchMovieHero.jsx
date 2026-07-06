import "./SearchMovieHero.css";
import { Link } from "react-router-dom";
const IMAGE = "https://image.tmdb.org/t/p/original";

function SearchMovieHero({ movie }) {

    if (!movie) return null;

    return (

        <div
            className="search-hero"
            style={{
                backgroundImage: `
                    linear-gradient(
                        to right,
                        rgba(0,0,0,.95),
                        rgba(0,0,0,.75),
                        rgba(0,0,0,.45)
                    ),
                    url(${IMAGE}${movie.backdrop})
                `
            }}
        >

            <div className="hero-content">

                <img

                    src={`${IMAGE}${movie.poster}`}

                    alt={movie.title}

                    className="hero-poster"

                />

                <div className="hero-info">

                    <h1>

                        {movie.title}

                    </h1>

                    <div className="hero-meta">

                        ⭐ {movie.rating?.toFixed(1)}

                        {

                            movie.release_date &&

                            <span>

                                {

                                    movie.release_date.substring(0,4)

                                }

                            </span>

                        }

                        {

                            movie.runtime &&

                            <span>

                                {movie.runtime} mins

                            </span>

                        }

                    </div>

                    {

                        movie.genres &&

                        <div className="genre-list">

                            {

                                movie.genres.map(g=>(

                                    <span

                                        key={g}

                                        className="genre-chip"

                                    >

                                        {g}

                                    </span>

                                ))

                            }

                        </div>

                    }

                    <p>

                        {movie.overview}

                    </p>

                    <Link

                        to={`/movie/${movie.id}`}

                        className="hero-btn"

                    >

                        View Details →

                    </Link>

                </div>

            </div>

        </div>

    );

}

export default SearchMovieHero;