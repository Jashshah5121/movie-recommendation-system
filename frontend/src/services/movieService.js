import API from "../api/axios";

export const getTrendingMovies = async () => {

    const { data } = await API.get("/movies/trending");

    return data;

};

export const getPopularMovies = async () => {

    const { data } = await API.get("/movies/popular");

    return data;

};

export const getTopRatedMovies = async () => {

    const { data } = await API.get("/movies/top-rated");

    return data;

};

export const getUpcomingMovies = async () => {

    const { data } = await API.get("/movies/upcoming");

    return data;

};

export async function searchMovies(query) {

    const response = await API.get(

        "/search",

        {
            params: {
                query
            }
        }

    );

    return response.data;

}

export const getMovieDetails = async (id) => {

    const { data } = await API.get(`/movies/${id}`);

    return data;

};

export const getRecommendations = async (id) => {

    const { data } = await API.get(
        `/movies/${id}/similar`
    );

    return data.results;

};

export const discoverMovies = async (filters) => {

    const { data } = await API.get(

        "/discover",

        {

            params: filters

        }

    );

    return data;

};

export async function smartSearch(query) {

    const { data } = await API.post(

        "/search/smart",

        {
            query
        }

    );

    return data;

}


export async function getWishlistRecommendations(movieIds) {

    const { data } = await API.post(
        "/recommendations/wishlist",
        {
            movie_ids: movieIds
        }
    );

    return data;
}

export async function getOnboardingMovies(languages = [], genres = []) {

    const params = new URLSearchParams();

    // Multiple languages
    if (languages.length > 0) {

        languages.forEach(lang => {

            params.append("language", lang);

        });

    }

    // Multiple genres
    if (genres.length > 0) {

        genres.forEach(genre => {

            params.append("genres", genre);

        });

    }

    const response = await fetch(

        `http://127.0.0.1:8000/movies/onboarding?${params.toString()}`

    );

    if (!response.ok) {

        throw new Error("Failed to fetch onboarding movies");

    }

    return response.json();

}

export async function getOnboardingRecommendations(profile) {

    const response = await fetch(

        "http://127.0.0.1:8000/recommendations/onboarding",

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(profile)

        }

    );

    if (!response.ok) {

        throw new Error("Failed to get onboarding recommendations");

    }

    return response.json();

}
export const autocompleteMovies = async (query) => {
    const { data } = await API.get("/search/autocomplete", {
        params: { query },
    });

    return data;
};