import "./FilterBar.css";

function FilterBar({

    filters,

    onChange

}) {

    return (

        <div className="filter-bar">

            <select
                value={filters.genre}
                onChange={(e) =>
                    onChange("genre", e.target.value)
                }
            >
                <option value="">All Genres</option>
                <option>Action</option>
                <option>Adventure</option>
                <option>Animation</option>
                <option>Comedy</option>
                <option>Crime</option>
                <option>Drama</option>
                <option>Fantasy</option>
                <option>Horror</option>
                <option>Mystery</option>
                <option>Romance</option>
                <option>Sci-Fi</option>
                <option>Thriller</option>
            </select>

            <select
                value={filters.language}
                onChange={(e) =>
                    onChange("language", e.target.value)
                }
            >
                <option value="">All Languages</option>
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="ko">Korean</option>
                <option value="ja">Japanese</option>
                <option value="fr">French</option>
            </select>

            <select
                value={filters.rating}
                onChange={(e) =>
                    onChange("rating", e.target.value)
                }
            >
                <option value="">Any Rating</option>
                <option value="9">9+</option>
                <option value="8">8+</option>
                <option value="7">7+</option>
                <option value="6">6+</option>
            </select>

            <select
                value={filters.sort}
                onChange={(e) =>
                    onChange("sort", e.target.value)
                }
            >
                <option value="popularity">
                    Popularity
                </option>

                <option value="rating">
                    Rating
                </option>

                <option value="newest">
                    Newest
                </option>

                <option value="oldest">
                    Oldest
                </option>

            </select>

        </div>

    );

}

export default FilterBar;