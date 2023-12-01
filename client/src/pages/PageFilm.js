import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import MessageForm from "../commentaire/MessageForm.js"; 
import Message from "../commentaire/Message.js";
import { useAuth } from "../AuthenticateContext.js";
import ImageFilm from "../search/ImageFilm.js";
import './PageFilm.css';

function PageFilm(props) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [isInWatchlist, setIsInWatchlist] = useState(false);

  const fetchComments = () => {
    fetch(`http://localhost:5000/api/comments?idFilm=${props.dataFilm.id}`, {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.comments);
            setComments(data.comments);
        })
        .catch((error) => console.log(error));
        }

  useEffect(() => {
    fetchComments();
  }, [props.dataFilm, setComments, setIsInWatchlist]);

  const handleNewMessage = (newMessage) => {
    setComments((prevComments) => [...prevComments, newMessage]);
  };

  const handleDeleteMessage = (deletedMessageId) => {
    setComments((prevComments) => prevComments.filter((msg) => msg.id !== deletedMessageId));
  };

  const addToWatchlist = () => {
    fetch('http://localhost:5000/watchlist/add', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ film_id: props.dataFilm.id }),
    })
      .then((response) => response.json())
      .then((data) => {
        setIsInWatchlist(!isInWatchlist);
      })
      .catch((error) => console.log(error));
  };

  const removeFromWatchlist = () => {
    fetch('http://localhost:5000/watchlist/remove', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ film_id: props.dataFilm.id }),
    })
      .then((response) => response.json())
      .then((data) => {
        setIsInWatchlist(!isInWatchlist);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div className="page-film-container">
      <header>
        <NavigationBar setPage={props.setPage} />
      </header>
      <main>
        <div className="film-details">
          <div className="film-poster">
            <ImageFilm dataFilm={props.dataFilm} setPage={props.setPage} />
          </div>
          <div className="film-info">
            <h1 className="titreMessage">
              {props.dataFilm.title ? props.dataFilm.title : props.dataFilm.name}
            </h1>
            <p>Sortie le : {props.dataFilm.release_date}</p>
            <p>{props.dataFilm.overview}</p>
            <button class="watchlist" onClick={isInWatchlist ? removeFromWatchlist : addToWatchlist}>
              {isInWatchlist ? "Retirer de ma WatchList" : "Ajouter à ma WatchList"}
            </button>
          </div>
        </div>
        <section>
          <div id="new_message">
            <MessageForm username={user} idFilm={props.dataFilm} updateMessage={handleNewMessage} />
          </div>
          <div>
            <h1 className="titreMessage">Commentaires</h1>
            {comments.map((message) => (
              <Message key={message.id} dataMessage={message} user_id={user} updateMessage={handleDeleteMessage} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default PageFilm;