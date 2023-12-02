import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import ImageFilm from "../search/ImageFilm";
import './watchlist.css'

function Watchlist() {
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    // Requête GET pour récupérer la Watchlist côté serveur
    fetch('http://localhost:5000/get-watchlist', {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => response.json())
      .then((data) => {
        setWatchlist(data.watchlist);
      })
      .catch((error) => console.log(error));
  }, []);

  return (
    <div className="watchlist-container">
      <header>
        <NavigationBar />
      </header>
        <div class="watchlist-content">
          <div class="posterwatchlist">
          <h2>Ma Watchlist</h2>
            {watchlist.map((item) => (
                <img class='img'
                src={`https://image.tmdb.org/t/p/w500/${item.poster_path}`}
                alt={item.title}
              />
            ))}
          </div>
      </div>
    </div>
  );
}

export default Watchlist;
