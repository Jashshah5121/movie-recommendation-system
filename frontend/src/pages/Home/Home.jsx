import { useEffect, useState } from "react";

import Hero from "../../components/Hero/Hero";
import MovieRow from "../../components/MovieRow/MovieRow";
import Loading from "../../components/Loading/Loading";

import {
    getTrendingMovies,
    getPopularMovies,
    getTopRatedMovies,
    getUpcomingMovies,
    getWishlistRecommendations
} from "../../services/movieService";

import useWishlist from "../../hooks/useWishlist";
import { useContext } from "react";
import { ProfileContext } from "../../context/ProfileContext";
import "../../styles/Home.css";

function Home() {

    const [trending, setTrending] = useState([]);
    const [popular, setPopular] = useState([]);
    const [topRated, setTopRated] = useState([]);
    const [upcoming, setUpcoming] = useState([]);
    const { wishlist } = useWishlist();
    const [personalized, setPersonalized] = useState([]);
    const [loading, setLoading] = useState(true);
    const { profile } = useContext(ProfileContext);
    // Current movie displayed in Hero
    const [heroIndex, setHeroIndex] = useState(0);

    // Load movies once
    useEffect(() => {

        async function loadMovies() {

            try {

                const [

                    trendingMovies,
                    popularMovies,
                    topRatedMovies,
                    upcomingMovies,
            

                ] = await Promise.all([

                    getTrendingMovies(),
                    getPopularMovies(),
                    getTopRatedMovies(),
                    getUpcomingMovies(),

                ]);

                setTrending(trendingMovies);
                setPopular(popularMovies);
                setTopRated(topRatedMovies);
                setUpcoming(upcomingMovies);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);

            }

        }

        loadMovies();

    }, []);

    useEffect(() => {

    async function loadWishlistRecommendations() {

        if (!wishlist.length) {

            setPersonalized([]);

            return;

        }

        try {

            const movieIds = wishlist.map(movie => movie.id);

            const recommendations =
                await getWishlistRecommendations(movieIds);

            setPersonalized(recommendations);

        }

        catch (err) {

            console.error(err);

        }

    }

    loadWishlistRecommendations();

}, [wishlist]);

    // Rotate Hero every 10 seconds
    useEffect(() => {

        if (trending.length === 0) return;

        const interval = setInterval(() => {

            setHeroIndex((prev) =>

                (prev + 1) % Math.min(5, trending.length)

            );

        }, 10000);

        return () => clearInterval(interval);

    }, [trending]);

    const heroMovie = trending[heroIndex];

    if (loading) {

        return <Loading />;

    }

return (

<div className="home">

    <Hero movie={heroMovie} />

    {
        profile.recommendedMovies &&
        profile.recommendedMovies.length > 0 && (

            <MovieRow
                title="❤️ Recommended For You"
                movies={profile.recommendedMovies}
            />

        )
    }

    {
        wishlist.length > 0 && (
            <MovieRow
                title="❤️ Based On Wishlist"
                movies={personalized}
            />
        )
    }

    <MovieRow
        title="🔥 Trending"
        movies={trending.slice(1)}
    />

    <MovieRow
        title="⭐ Popular"
        movies={popular}
    />

    <MovieRow
        title="🏆 Top Rated"
        movies={topRated}
    />

    <MovieRow
        title="🎬 Upcoming"
        movies={upcoming}
    />

</div>

);

}

export default Home;