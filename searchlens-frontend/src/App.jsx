import React from "react";
import SearchBar from "./components/SearchBar";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <SearchBar />
        </div>
      </header>
    </div>
  );
}
