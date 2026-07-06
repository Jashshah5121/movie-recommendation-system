import { useNavigate } from "react-router-dom";
import "./Onboarding.css";

function Welcome() {

    const navigate = useNavigate();

    return (

        <div className="onboarding-page">

            <div className="onboarding-card">

                <div className="logo">🎬</div>

                <h1>Welcome to MovieHub</h1>

                <p>
                    Your personal AI movie assistant.
                </p>

                <p className="subtitle">
                    We'll learn your movie taste and create
                    recommendations made just for you.
                </p>

                <button
                    className="primary-btn"
                    onClick={() => navigate("/onboarding/genres")}
                >
                    Get Started →
                </button>

            </div>

        </div>

    );

}

export default Welcome;