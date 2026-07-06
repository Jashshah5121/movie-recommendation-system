import "./Navbar.css";

import { Link } from "react-router-dom";

import useWishlist from "../../hooks/useWishlist";

import {
  Search,
  Heart,
  Compass,
  Sparkles
} from "lucide-react";

function Navbar() {

  const { wishlist } = useWishlist();

  return (

    <nav className="navbar">

      <Link to="/" className="logo">
        MovieHub
      </Link>

      <div className="nav-links">

        <Link to="/">
          Home
        </Link>

        <Link to="/discover">
          <Compass size={18} />
          Discover
        </Link>

        <Link to="/wishlist">
          <Heart size={18} />
          Wishlist

          {wishlist.length > 0 && (
            <span className="wishlist-count">
              {wishlist.length}
            </span>
          )}

        </Link>

        <Link to="/recommend">
          <Sparkles size={18} />
          AI Recommend
        </Link>

      </div>

    </nav>

  );

}

export default Navbar;