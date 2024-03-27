import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import './watchlist.css'
import ImageFilm from "../search/ImageFilm";

function Watchlist(props) {
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    // Requête GET pour récupérer la Watchlist côté serveur
    fetch('http://localhost:5000/watchlist/get-watchlist', {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setWatchlist(data.watchlist);
      })
      .catch((error) => console.log(error));
  }, []);

  return (
    <div className="watchlist-container">
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
    <div className="watchlist-content">
    <h2>Ma Watchlist</h2>
          <div className="posterwatchlist">
            {watchlist.map((item) => (
              <div key={item.id}>
              <ImageFilm dataFilm={item} setPage={props.setPage} />
              </div>
            ))}
          </div>
      </div>
    </div>
  );
}

export default Watchlist;
