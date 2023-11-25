//import { useState, useEffect } from "react";
import NavigationBar from "../NavigationBar";
import './Search.css'


function Search(props){
    //const [userId, setUserId] = useState(); 
    //const {user,loading}= useAuth();


    const handleClickImageFilm = (i) =>{
      console.log(i.id)
      props.setPage(["film_page", i])
    }
    /*useEffect(() => {
        const fetchIsconnected = ()=>{
          fetch(`http://localhost:5000/@me`, {
              headers: {"Content-Type": "application/json"}
            }
          )
          .then((response)=> response.json())
          .then((data)=>{
            // s'il y a des données dans la response.
            console.log(data)
            setUserId(data.id); // Initialize with an empty array if results are undefined
          })
          .catch((error)=> console.log(error))
      };
      fetchIsconnected();
    
    }, []);
    */
    
    return (
    <div>
        <header>
            <NavigationBar setPage={props.setPage}></NavigationBar>
        </header>
        <div className="SearchPage">
        <h2>Résultats</h2>
        <div className="results">
          {props.datasearch.results.map((movie) => (
            // Vérifiez si le film a un poster_path avant de l'afficher
            movie.poster_path && (
              <div key={movie.id} class="resultsearch">
                <img
                  class="search-results"
                  src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                  alt={movie.title}
                  onClick={() => handleClickImageFilm(movie)}
                />
              </div>
            )
          ))}
        </div>
      </div>
    </div>
    ); 
}

export default Search; 