import { useEffect, useState } from "react";

import FilterBar from "../../components/FilterBar/FilterBar";
import MovieGrid from "../../components/MovieGrid/MovieGrid";

import API from "../../api/axios";

import "./Discover.css";

function Discover() {

    const [movies, setMovies] = useState([]);

    const [loading, setLoading] = useState(true);

    const [filters, setFilters] = useState({

        genre: "",

        language: "",

        rating: "",

        sort: "popularity"

    });

    useEffect(() => {

        loadMovies();

    }, [filters]);

    async function loadMovies() {

        try {

            setLoading(true);

            const { data } = await API.get("/discover", {

                params: {

                    genre: filters.genre,

                    language: filters.language,

                    min_rating: filters.rating,

                    sort: filters.sort

                }

            });

            setMovies(data);

        }

        catch (err) {

            console.error(err);

        }

        finally {

            setLoading(false);

        }

    }

    function handleFilterChange(key, value) {

        setFilters(prev => ({

            ...prev,

            [key]: value

        }));

    }

    return (

        <div className="discover-page">

            <h1>

                Discover Movies

            </h1>

            <FilterBar

                filters={filters}

                onChange={handleFilterChange}

            />

            {

                loading ?

                (

                    <h2>

                        Loading...

                    </h2>

                )

                :

                (

                    <MovieGrid

                        movies={movies}

                    />

                )

            }

        </div>

    );

}

export default Discover;