import { createContext, useEffect, useState } from "react";

export const WishlistContext = createContext();

export function WishlistProvider({ children }) {

    const [wishlist, setWishlist] = useState([]);

    // Load wishlist from localStorage
    useEffect(() => {

        const saved = localStorage.getItem("wishlist");

        if (saved) {

            setWishlist(JSON.parse(saved));

        }

    }, []);

    // Save whenever wishlist changes
    useEffect(() => {

        localStorage.setItem(
            "wishlist",
            JSON.stringify(wishlist)
        );

    }, [wishlist]);

    // Add movie
    function addMovie(movie) {

        setWishlist(prev => {

            if (prev.find(m => m.id === movie.id)) {

                return prev;

            }

            return [...prev, movie];

        });

    }

    // Remove movie
    function removeMovie(id) {

        setWishlist(prev =>

            prev.filter(movie => movie.id !== id)

        );

    }

    // Toggle
    function toggleWishlist(movie) {

        const exists = wishlist.some(

            m => m.id === movie.id

        );

        if (exists) {

            removeMovie(movie.id);

        } else {

            addMovie(movie);

        }

    }

    function isWishlisted(id) {

        return wishlist.some(

            movie => movie.id === id

        );

    }

    return (

        <WishlistContext.Provider
            value={{
                wishlist,
                addMovie,
                removeMovie,
                toggleWishlist,
                isWishlisted
            }}
        >

            {children}

        </WishlistContext.Provider>

    );

}