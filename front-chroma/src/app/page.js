"use client";

import Image from "next/image";
import { useState } from "react";
import styles from "./globals.css";
import InputField from "./components/InputField";
import MovieList from "./components/MovieList";
import SubmitButton from "./components/SubmitButton";

export default function Home() {
  const [input, setInput] = useState("");
  const [movies, setMovies] = useState([]);

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleButtonClick = () => {
    // Perform some action with the input value
    // and update the movies state accordingly
    // Example:
    fetchMovies(input)
      .then((movies) => setMovies(movies))
      .catch((error) => console.log(error));
  };

  const fetchMovies = (query) => {
    // Implement your logic to fetch movies based on the query
    // and return a promise that resolves with the movies data
    // Example:
    return fetch(`https://api.example.com/movies?query=${query}`)
      .then((response) => response.json())
      .then((data) => data.results)
      .catch((error) => console.log(error));
  };

  return (
    <main className="wrapper">
      <div className="container">
        <div>
          <h1>This: GPT4ALL + Vectorial database</h1>
        </div>
        <InputField value={input} onChange={handleInputChange} />
        <SubmitButton onClick={handleButtonClick} className="btn" />
        {movies.length > 0 && <MovieList movies={movies} />}
      </div>
    </main>
  );
}
