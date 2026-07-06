import Home from "./pages/Home/Home.jsx";
import MovieDetails from "./pages/MovieDetails.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";

import {
    Routes,
    Route,
    Navigate,
    useLocation
} from "react-router-dom";

import { useContext } from "react";

import Wishlist from "./pages/Wishlist/Wishlist";
import Discover from "./pages/Discover/Discover";
import AIRecommend from "./pages/AIRecommend/AIRecommend";

import Welcome from "./pages/Onboarding/Welcome";
import Genres from "./pages/Onboarding/Genres";
import Languages from "./pages/Onboarding/Languages";
import FavoriteMovies from "./pages/Onboarding/FavoriteMovies";

import { ProfileContext } from "./context/ProfileContext";

function App() {

    const { profile } = useContext(ProfileContext);

    const location = useLocation();

    const hideNavbar =
        location.pathname === "/welcome" ||
        location.pathname.startsWith("/onboarding");

    return (
        <>

            {!hideNavbar && <Navbar />}

            <Routes>

                {/* ---------------- Onboarding ---------------- */}

                <Route
                    path="/welcome"
                    element={<Welcome />}
                />

                <Route
                    path="/onboarding/genres"
                    element={<Genres />}
                />

                <Route
                    path="/onboarding/languages"
                    element={<Languages />}
                />

                <Route
                    path="/onboarding/movies"
                    element={<FavoriteMovies />}
                />

                {/* ---------------- Main App ---------------- */}

                <Route
                    path="/"
                    element={
                        profile.completed
                            ? <Home />
                            : <Navigate to="/welcome" replace />
                    }
                />

                <Route
                    path="/movie/:id"
                    element={<MovieDetails />}
                />

                <Route
                    path="/wishlist"
                    element={<Wishlist />}
                />

                <Route
                    path="/discover"
                    element={<Discover />}
                />

                <Route
                    path="/recommend"
                    element={<AIRecommend />}
                />

            </Routes>

        </>
    );
}

export default App;