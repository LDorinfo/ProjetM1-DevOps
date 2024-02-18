import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import MessageForm from "../commentaire/MessageForm.js"; 
import Message from "../commentaire/Message.js";
import { useAuth } from "../AuthenticateContext.js";
import ImageFilm from "../search/ImageFilm.js";
import './PageFilm.css';
import NoteStars from "../commentaire/NoteStars.js";
import { useParams, useLocation } from "react-router-dom"; 

function PageFilm(props) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [meanGrade, setMeanGrade]= useState(0); 
  const { filmId } = useParams();
  //const location = useLocation(); Utilisez useLocation pour accéder aux paramètres d'emplacement
  //const filmData = location.state.filmData; // Accédez aux données du film à partir des paramètres d'emplacement
  const filmData = props.dataFilm;
  const fetchComments = () => {
    fetch(`http://localhost:5000/comments/comments?idFilm=${filmId}`, {
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

  const updateGrade = ()=>{
    // utilisation de useEffect pour mettre à jour la note du film à chaque fois qu'un commentaire est ajouté de la liste comments ou supprimer
    const totalGrade = comments.reduce((sum, comment) => sum + comment.note, 0);
    // utilisation d'un lambda
    const averageGrade = totalGrade / comments.length || 0;
    setMeanGrade(averageGrade);
  }

  const handleNewMessage = (newMessage) => {
    setComments((prevComments) => [...prevComments, newMessage]);
    updateGrade(); 
  };

  const handleDeleteMessage = (deletedMessageId) => {
    setComments((prevComments) => prevComments.filter((msg) => msg.id !== deletedMessageId));
    updateGrade(); 
  };


  const addToWatchlist = () => {
    fetch('http://localhost:5000/watchlist/add', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        film_id: filmId,
        title: filmData.title, // ou name selon votre structure de données
        poster_path: filmData.poster_path,
      }),
    })
    .then((response) => response.json())
    .then((data) => {
        setIsInWatchlist(!isInWatchlist);
    })
    .catch((error) => console.log(error));
  };

  const removeFromWatchlist = () => {
    fetch('http://localhost:5000/watchlist/remove', {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ film_id: filmId}),
    })
      .then((response) => response.json())
      .then((data) => {
        setIsInWatchlist(!isInWatchlist);
      })
      .catch((error) => console.log(error));
  };

  const fetchMediaVideos = () => {
    fetch('http://localhost:5000/get-trailer', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: filmId,
        media_type: filmData.media_type,
      }),
    })
    .then((response) => response.json())
    .then((data) => {
      const videos = data.videos;
  
      // Si des vidéos sont disponibles, ouvrez le lien de la première vidéo 
      if (videos && videos.length > 0) {
        const videoKey = videos[0].key;
        window.open(`https://www.youtube.com/watch?v=${videoKey}`, '_blank');
      } else {
        // Aucune vidéo disponible
        console.log("Aucune vidéo disponible");
      }
    })
    .catch((error) => console.log(error));
  };     

  useEffect(() => {
    fetchComments();
  }, [filmData, setComments, setIsInWatchlist]);

  useEffect(()=>{
    updateGrade(); 
  }, [comments]);


  return (
    <div className="page-film-container">
      <header>
        <NavigationBar />
      </header>
      <main>
        <div className="film-details">
          <div className="film-poster">
            <ImageFilm dataFilm={filmData} />
          </div>
          <div className="film-info">
            <h1 className="titreMessage">
              {filmData.title ? filmData.title : filmData.name}
            </h1>
            <p>Sortie le : {filmData.release_date}    <a className="bandeannonce" onClick={fetchMediaVideos}>Bande annonce</a></p>

            <p>{filmData.overview}</p>
            <div className="mean-grade">
              <NoteStars noteUser={meanGrade} isClickable={false}/>
              <p>{meanGrade} / 5</p>
            </div>
            {user ? (
              <button className="watchlist" onClick={isInWatchlist ? removeFromWatchlist : addToWatchlist}>
                {isInWatchlist ? "Retirer de ma WatchList" : "Ajouter à ma WatchList"}
              </button>
            ) : (
              <p className="msg">Connectez-vous pour l'ajouter à votre Watchlist !</p>
            )}
          </div>
        </div>
        <section>
          <div id="new_message">
            <MessageForm username={user} idFilm={filmId} updateMessage={handleNewMessage}/>
          </div>
          <div>
            <h1 className="titreMessage">Commentaires</h1>
            {comments.map((message) => (
              <Message key={message.id} dataMessage={message} user_id={user} updateMessage={handleDeleteMessage} updateTextMessage={fetchComments}/>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default PageFilm;