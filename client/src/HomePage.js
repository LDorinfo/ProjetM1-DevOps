import { useState, useEffect } from "react";
import './HomePage.css'
import NavigationBar from "./NavigationBar";


function HomePage(props) {
  const [connectedUsers, setConnectedUsers] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);

  useEffect(() => {
    const fetchConnectedUsers = () => {
      fetch(`http://localhost:5000/api/users/connected?id=${props.user_id}`, {
        method: 'GET',
        headers: {"Content-Type": "application/json"},

      })
      //Get ne prend pas de body dans sa requête. 
        .then(response => response.json())
        .then(data => {
          if (data.status === 200) {
            setConnectedUsers(data.isconnected);
          }
        })
        .catch(error => console.log(error));
    };
    
    const fetchPopularMovies = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/trending-movies', {
          method: 'GET',
          headers: {"Content-Type": "application/json"}
        }
        )
        if (response.ok) {
          const data = await response.json();
          setPopularMovies(data.results || []); // Initialize with an empty array if results are undefined
        } else {
          console.error('Erreur lors de la récupération des films populaires');
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des films populaires', error);
      }
    };
    fetchConnectedUsers();
    fetchPopularMovies();

  }, []);

  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}></NavigationBar>
      </header>
      <div class="HomePage">
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