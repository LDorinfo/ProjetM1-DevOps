import React, { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import MessageForm from "../commentaire/MessageForm.js"; 
import Message from "../commentaire/Message.js";
import { useAuth } from "../AuthenticateContext.js";
import ImageFilm from "../search/ImageFilm.js";
import './PageFilm.css';
import NoteStars from "../commentaire/NoteStars.js";

function PageFilm(props) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [meanGrade, setMeanGrade]= useState(0); 
  const [isInWatchlist, setIsInWatchlist] = useState(false); 
  const [providers, setProviders] = useState(null); // State pour stocker les fournisseurs

  const fetchComments = () => {
    fetch(`http://localhost:5000/comments/comments?idFilm=${props.dataFilm.id}`, {
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
  const getGenreString = () => {
    if (props.dataFilm.info.genres) {
      return props.dataFilm.info.genres.map(genre => genre.name).join(", ");
    }
    return "";
  };

  const addToWatchlist = () => {
    
    fetch('http://localhost:5000/watchlist/add', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        film_id: props.dataFilm.id,
        title: props.dataFilm.title, // ou name selon votre structure de données
        poster_path: props.dataFilm.poster_path,
        type : props.dataFilm.media_type,
        genres : getGenreString()
      }),
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
        setIsInWatchlist(!isInWatchlist);
    })
    .catch((error) => console.log(error));
  };

  const removeFromWatchlist = () => {
    fetch('http://localhost:5000/watchlist/remove', {
      method: 'DELETE',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ film_id: props.dataFilm.id, type : props.dataFilm.media_type }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
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
        id: props.dataFilm.id,
        media_type: props.dataFilm.media_type,
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
  const fetchIsInWatchlist =  () => {
    fetch(`http://localhost:5000/watchlist/check-in-watchlist?film_id=${props.dataFilm.id}`, {
        method: 'GET',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
    })
    .then((response) => response.json())
    .then((data) => {
      setIsInWatchlist(data.in_watchlist);
    })
    .catch((error) => console.log(error));
  };     

  useEffect(() => {
    fetchIsInWatchlist();
  }, [props.dataFilm]); // Effectue la vérification chaque fois que props.dataFilm change

  const fetchMediaProviders = () => {
    fetch('http://localhost:5000/get-providers', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: props.dataFilm.id,
      }),
    })
    .then((response) => response.json())
    .then((data) => {
      const providersData = data.providers;
      setProviders(providersData); // Mettre à jour le state avec les données des fournisseurs
    })
    .catch((error) => console.log(error));
  };  

  useEffect(() => {
    fetchComments();
    fetchMediaProviders(); // Appel à la fonction pour récupérer les fournisseurs lors du chargement du composant
  }, [props.dataFilm, setComments, setIsInWatchlist]);

  useEffect(()=>{
    updateGrade(); 
  }, [comments]);


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
            <h1 className="titreFilm">
              {props.dataFilm.title ? props.dataFilm.title : props.dataFilm.name}
            </h1>
            <p>Sortie le : {props.dataFilm.release_date}    <a className="bandeannonce" onClick={fetchMediaVideos}>Bande annonce</a></p>
            <p>{props.dataFilm.overview}</p>
            {providers && (
              <div className="provider-logos">
                {providers.flatrate && providers.flatrate.map(provider => (
                  <img key={provider.provider_id} src={`https://image.tmdb.org/t/p/original${provider.logo_path}`} alt={provider.provider_name} />
                ))}
                {providers.buy && providers.buy.map(provider => (
                  <img key={provider.provider_id} src={`https://image.tmdb.org/t/p/original${provider.logo_path}`} alt={provider.provider_name} />
                ))}
              </div>
            )}
            <div className="tmdb-grade">
            <p>Notes TMDB : {Math.round(props.dataFilm.info.vote_average * 10)}%</p>
            </div>
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
            <MessageForm username={user} idFilm={props.dataFilm} updateMessage={handleNewMessage}/>
          </div>
          <div>
            <h1 className="titreMessage">Commentaires</h1>
            {comments.map((message) => (
              <Message key={message.id} dataMessage={message} user_id={user} updateMessage={handleDeleteMessage} updateTextMessage={fetchComments}/>
            ))}
          </div>
        </section>
        {/* Affichage des logos des fournisseurs */}
      </main>
    </div>
  );
}

export default PageFilm;