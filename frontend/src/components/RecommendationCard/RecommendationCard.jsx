import "./RecommendationCard.css";
import { Link } from "react-router-dom";
import { Star, Sparkles, Brain } from "lucide-react";

const IMAGE_BASE = "https://image.tmdb.org/t/p/w500";

function RecommendationCard({ movie }) {

    const explanation = movie.explanation || {};

    const confidence = explanation.confidence || null;

    const summary = explanation.summary || "";

    const reasons = explanation.why || [];

    return (

        <Link
            to={`/movie/${movie.id}`}
            className="recommendation-link"
        >

            <div className="recommendation-card">

                <img
                    src={`${IMAGE_BASE}${movie.poster}`}
                    alt={movie.title}
                    className="recommendation-poster"
                />

                <div className="recommendation-info">

                    <div className="recommendation-header">

                        <h2>{movie.title}</h2>
                        <p className="movie-year">
                            {movie.year}
                        </p>

                        {confidence && (

                            <div className="match-pill">

                                <Sparkles size={16}/>

                                {confidence}% Match

                            </div>

                        )}

                    </div>

                    <div className="recommendation-rating">

                        <Star
                            size={18}
                            fill="gold"
                        />

                        {movie.rating?.toFixed(1)}

                    </div>

                    {

                        summary && (

                            <div className="summary-box">

                                <Brain size={18}/>

                                <p>{summary}</p>

                            </div>

                        )

                    }

                    {

                        reasons.length>0 && (

                            <>

                                <h4>

                                    Why this movie?

                                </h4>

                                <div className="reason-list">

                                    {

                                        reasons.map((reason,index)=>(

                                            <span
                                                key={index}
                                                className="reason"
                                            >

                                                {reason}

                                            </span>

                                        ))

                                    }

                                </div>

                            </>

                        )

                    }

                    <button className="more-btn">

                        View Details →

                    </button>

                </div>

            </div>

        </Link>

    );

}

export default RecommendationCard;