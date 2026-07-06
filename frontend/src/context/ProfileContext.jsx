import { createContext, useEffect, useState } from "react";

export const ProfileContext = createContext();

const defaultProfile = {
    completed: false,
    genres: [],
    languages: [],
    likedMovies: [],
    recommendedMovies: []
};

export function ProfileProvider({ children }) {

    const [profile, setProfile] = useState(defaultProfile);

    useEffect(() => {
        const saved = localStorage.getItem("movieProfile");

        if (saved) {
            setProfile(JSON.parse(saved));
        }
    }, []);

    useEffect(() => {
        localStorage.setItem(
            "movieProfile",
            JSON.stringify(profile)
        );
    }, [profile]);

    function updateGenres(genres) {
        setProfile(prev => ({
            ...prev,
            genres
        }));
    }

    function updateLanguages(languages) {
        setProfile(prev => ({
            ...prev,
            languages
        }));
    }

    function updateLikedMovies(likedMovies) {
        setProfile(prev => ({
            ...prev,
            likedMovies
        }));
    }

    function updateRecommendedMovies(recommendedMovies) {
        setProfile(prev => ({
            ...prev,
            recommendedMovies
        }));
    }

    function completeOnboarding() {
        setProfile(prev => ({
            ...prev,
            completed: true
        }));
    }

    function resetProfile() {
        localStorage.removeItem("movieProfile");
        setProfile(defaultProfile);
    }

    return (
        <ProfileContext.Provider
            value={{
                profile,
                updateGenres,
                updateLanguages,
                updateLikedMovies,
                updateRecommendedMovies,
                completeOnboarding,
                resetProfile
            }}
        >
            {children}
        </ProfileContext.Provider>
    );
}