import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ProfileContext } from "../../context/ProfileContext";
import "./Onboarding.css";

const LANGUAGES = [
    { name: "English", code: "en", flag: "🇺🇸" },
    { name: "Hindi", code: "hi", flag: "🇮🇳" },
    { name: "Japanese", code: "ja", flag: "🇯🇵" },
    { name: "Korean", code: "ko", flag: "🇰🇷" },
    { name: "Chinese", code: "zh", flag: "🇨🇳" },
    { name: "French", code: "fr", flag: "🇫🇷" },
    { name: "German", code: "de", flag: "🇩🇪" },
    { name: "Italian", code: "it", flag: "🇮🇹" },
    { name: "Spanish", code: "es", flag: "🇪🇸" },
    { name: "Turkish", code: "tr", flag: "🇹🇷" }
];
function Languages() {

    const navigate = useNavigate();

    const { updateLanguages } = useContext(ProfileContext);

    const [selected, setSelected] = useState([]);

    function toggleLanguage(language) {

        if (selected.includes(language)) {

            setSelected(
                selected.filter(l => l !== language)
            );

        } else {

            setSelected([...selected, language]);

        }

    }

    function handleContinue() {

        if (selected.length === 0) {

            alert("Please select at least one language.");

            return;

        }

        updateLanguages(selected);

        navigate("/onboarding/movies");

    }

    return (

        <div className="onboarding-page">

            <div className="onboarding-card large-card">

                <div className="step">
                    Step 2 of 4
                </div>

                <h1>Preferred Languages</h1>

                <p className="subtitle">
                    Choose the languages you enjoy watching.
                </p>

                <div className="chip-grid">

                    {LANGUAGES.map(language => (

                        <button
                            key={language.code}
                            className={
                                selected.includes(language.code)
                                    ? "genre-chip active"
                                    : "genre-chip"
                            }
                            onClick={() =>
                                toggleLanguage(language.code)
                            }
                        >

                            <span className="genre-icon">
                                {language.flag}
                            </span>

                            {language.name}

                        </button>

                    ))}

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

export default Languages;