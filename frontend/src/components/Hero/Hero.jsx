import "./Hero.css";
import { Link } from "react-router-dom";

export default function Hero({ movie }) {

    console.log("Hero Movie:", movie);

    if (!movie) return null;


const backdrop = movie.backdrop
    ? `https://image.tmdb.org/t/p/original${movie.backdrop}`
    : movie.poster
    ? `https://image.tmdb.org/t/p/w780${movie.poster}`
    : "https://placehold.co/1600x900";

  return (
    <section
      className="hero"
      style={{
        backgroundImage: `url(${backdrop})`,
      }}
    >
      <div className="hero-overlay">

        <div className="hero-content">

          <h1>{movie.title}</h1>
          {movie.tagline && (

            <h3 className="hero-tagline">

                {movie.tagline}

            </h3>

        )}

          <div className="hero-meta">

            <span>⭐ {movie.rating?.toFixed(1)}</span>

            <span>{movie.release_date?.slice(0,4)}</span>

          </div>

          <p>
            {movie.overview}
          </p>

          <div className="hero-buttons">

            <a
              href={`https://www.youtube.com/results?search_query=${movie.title}+trailer`}
              target="_blank"
              rel="noreferrer"
              className="watch-btn"
            >
              ▶ Watch Trailer
            </a>

            <Link
              to={`/movie/${movie.id}`}
              className="info-btn"
            >
              More Info
            </Link>

          </div>

        </div>

      </div>

    </section>
  );
}