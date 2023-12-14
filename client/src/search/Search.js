//import { useState, useEffect } from "react";
import NavigationBar from "../NavigationBar";
import ImageFilm from "./ImageFilm";
import './Search.css'


function Search(props){
    //const [userId, setUserId] = useState(); 
    //const {user,loading}= useAuth();

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
              <div key={movie.id} className="resultsearch">
                <ImageFilm dataFilm={movie} setPage={props.setPage}/>
              </div>
            )
          ))}
        </div>
      </div>
    </div>
    ); 
}

export default Search; 