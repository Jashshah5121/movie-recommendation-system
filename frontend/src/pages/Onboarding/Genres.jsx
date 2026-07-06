import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ProfileContext } from "../../context/ProfileContext";
import "./Onboarding.css";

const GENRES = [
    { name: "Action", icon: "💥" },
    { name: "Adventure", icon: "🏴‍☠️" },
    { name: "Animation", icon: "🎨" },
    { name: "Comedy", icon: "😂" },
    { name: "Crime", icon: "🔫" },
    { name: "Drama", icon: "🎭" },
    { name: "Fantasy", icon: "🧙" },
    { name: "Family", icon: "👨‍👩‍👧" },
    { name: "Horror", icon: "👻" },
    { name: "Music", icon: "🎵" },
    { name: "Romance", icon: "❤️" },
    { name: "Sci-Fi", icon: "🚀" },
    { name: "Sports", icon: "⚽" },
    { name: "Thriller", icon: "🕵️" }
];

function Genres() {

    const navigate = useNavigate();

    const { updateGenres } = useContext(ProfileContext);

    const [selected, setSelected] = useState([]);

    function toggleGenre(genre) {

        if (selected.includes(genre)) {

            setSelected(
                selected.filter(g => g !== genre)
            );

        } else {

            setSelected([...selected, genre]);

        }

    }

    function handleContinue() {

        if (selected.length < 3) {

            alert("Please select at least 3 genres.");

            return;

        }

        updateGenres(selected);

        navigate("/onboarding/languages");

    }

    return (

        <div className="onboarding-page">

            <div className="onboarding-card large-card">

                <div className="step">
                    Step 1 of 4
                </div>

                <h1>Choose Your Favorite Genres</h1>

                <p className="subtitle">
                    Select at least 3 genres you enjoy.
                </p>

                <div className="chip-grid">

                    {
                        GENRES.map((genre) => (

                            <button
                                key={genre.name}
                                className={
                                    selected.includes(genre.name)
                                        ? "genre-chip active"
                                        : "genre-chip"
                
                                }
                                onClick={() => toggleGenre(genre.name)}
                            >

                                <span className="genre-icon">
                                        {genre.icon}
                                </span>

                                    {genre.name}

                            </button>

                        ))
                    }

                </div>

                <button
                    className="primary-btn"
                    onClick={handleContinue}
                >
                    Continue →
                </button>

            </div>

        </div>

    );

}

export default Genres;