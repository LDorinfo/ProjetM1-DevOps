import { useState, useEffect } from "react";
import './HomePage.css'
import NavigationBar from "./NavigationBar";


function HomePage(props) {
  const [popularMovies, setPopularMovies] = useState([]);

  useEffect(() => {
    const fetchPopularMovies = ()=>{
      fetch('http://localhost:5000/api/trending-movies', {
          method: 'GET',
          headers: {"Content-Type": "application/json"}
        }
      )
      .then((response)=> response.json())
      .then((data)=>{
        // s'il y a des données dans la response.
        console.log(data)
        setPopularMovies(data || []); // Initialize with an empty array if results are undefined
      })
      .catch((error)=> console.log(error))
  };
  fetchPopularMovies();

  }, []);

  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage} user_id={props.user_id}></NavigationBar>
      </header>
      <div className="HomePage">
        <div className="text-container">  
          <p>Dive into CineVerse: films, séries, animes. Votre univers de divertissement</p>
          <img src="/wordpress-cs-format-image-20.webp" alt="Description de l'image" />]
        </div>
        <section className="trending-movies">
          <h2>Films tendances <img src="https://img.icons8.com/fluency/48/star--v1.png" alt="star--v1"/></h2>
          <div className="movies-list">
            {popularMovies.map((movie) => (
              <div key={movie.id}>
              <h2>{movie.title}</h2>
              <p>{movie.overview}</p>
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} // Utilisez poster_path ou backdrop_path selon votre préférence
                alt={movie.title}
              />
            </div>
          ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default HomePage;