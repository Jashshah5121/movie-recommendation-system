import "./Wishlist.css";

import MovieCard from "../../components/MovieCard/MovieCard";

import useWishlist from "../../hooks/useWishlist";

function Wishlist() {

    const { wishlist } = useWishlist();

    return (

        <div className="wishlist-page">

            <div className="wishlist-header">

                <h1>❤️ My Wishlist</h1>

                <p>

                    {wishlist.length}

                    {" "}

                    Movie{wishlist.length !== 1 ? "s" : ""}

                    {" "}Saved

                </p>

            </div>

            {

                wishlist.length === 0 ?

                (

                    <div className="wishlist-empty">

                        <h2>Your Wishlist is Empty</h2>

                        <p>

                            Click the ❤️ icon on any movie to save it.

                        </p>

                    </div>

                )

                :

                (

                    <div className="wishlist-grid">

                        {

                            wishlist.map(movie => (

                                <MovieCard

                                    key={movie.id}

                                    movie={movie}

                                />

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}

export default Wishlist;