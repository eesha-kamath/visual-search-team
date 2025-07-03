import React from "react";
import { FaSearch, FaCamera } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const SearchBar = () => {
  const navigate = useNavigate();
  return (
    <div className="search-bar-wrapper">
      <div className="input-with-search">
        <input
          type="text"
          placeholder="Search everything at Walmart online and in store"
          className="search-input"
        />
        <button className="search-button" aria-label="Search">
          <FaSearch size={16} color="#fff" />
        </button>
      </div>

      <button className="camera-button" aria-label="Camera" onClick={() => navigate("/lens")}>
        <FaCamera size={20} color="#004f9a" />
      </button>
    </div>
  );
};

export default SearchBar;
