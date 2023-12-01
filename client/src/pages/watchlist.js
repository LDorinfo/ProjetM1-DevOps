import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import ImageFilm from "../search/ImageFilm";
// j'ai enlevé le css car il n'y en a pas encore
function Watchlist(props) {
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    // Récupérer la Watchlist depuis le backend
    fetch('http://localhost:5000/watchlist', {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.watchlist);
        setWatchlist(data.watchlist);
      })
      .catch((error) => console.log(error));
  }, []);

  return (
    <div className="watchlist-container">
      <header>
        <NavigationBar />
      </header>
      <main>
        <h1>Ma Watchlist</h1>
        <div className="watchlist-movies">
          {watchlist.map((movie) => (
            <div key={movie.id} className="watchlist-movie">
              <ImageFilm dataFilm={movie} />
              <h3>{movie.title}</h3>
              <p>Sortie le : {movie.release_date}</p>
              <p>{movie.overview}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default Watchlist;
