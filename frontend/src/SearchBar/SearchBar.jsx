import { useEffect, useState } from "react";
import "./SearchBar.css";
import { autocompleteMovies } from "../services/movieService";

export default function SearchBar({
  query,
  setQuery,
  onSearch,
  loading,
  onMovieSelect,
}) {
  const [suggestions, setSuggestions] = useState([]);
  const [isAutocompleting, setIsAutocompleting] = useState(false);

  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsAutocompleting(true);

      try {
        const data = await autocompleteMovies(query);
        // Problem 3 Fix: Log the fetched movies to the console
        console.log(data);
        setSuggestions(data);
      } catch (error) {
        console.error("Autocomplete failed:", error);
      } finally {
        setIsAutocompleting(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      onSearch();
      setSuggestions([]); // Close dropdown on search
    }
  };

  const exampleQueries = [
    "Interstellar",
    "Racing Movies",
    "Movies like Avatar",
    "Movie where toys come alive",
    "Tom Cruise movies",
    "Christopher Nolan movies",
  ];

  return (
    <div className="search-bar-section">
      <div className="search-heading">
        <h1>🤖 MovieHub AI</h1>
        <p>
          Search any movie, actor, director or simply describe a movie you
          remember.
        </p>
      </div>

      {/* Problem 2 Fix: Added search-input-wrapper to isolate input & dropdown from the button */}
      <div className="search-input-row">
        <div className="search-input-wrapper">
          <input
            type="text"
            placeholder="Search movies naturally..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />

          {/* --- Autocomplete Dropdown --- */}
          {suggestions.length > 0 && (
            <div className="search-dropdown">
              {suggestions.map((movie) => (
                <div
                  key={movie.id}
                  className="search-item"
                  onMouseDown={() => {
                    setQuery(movie.title);

                    if (onMovieSelect) {
                      onMovieSelect(movie);
                    }
                    setSuggestions([]);
                  }}
                >
                  {movie.poster && (
                    <img src={movie.poster} alt={movie.title} />
                  )}

                  <div>
                    <h4>{movie.title}</h4>
                    <p>{movie.year}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <button
          onClick={() => {
            onSearch();
            setSuggestions([]);
          }}
          disabled={loading}
        >
          {loading ? "Searching..." : "🔍 Search"}
        </button>
      </div>

      <div className="example-searches">
        {exampleQueries.map((item) => (
          <button
            key={item}
            onClick={() => {
              setQuery(item);
              setTimeout(onSearch, 100);
              setSuggestions([]);
            }}
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}