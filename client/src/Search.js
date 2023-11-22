import { useState, useEffect } from "react";
import NavigationBar from "./NavigationBar";

function Search(props){
    const [userId, setUserId] = useState(); 

    useEffect(() => {
        const fetchIsconnected = ()=>{
          fetch('http://localhost:5000/api/@me', {
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
    
    
    return (
    <div>
        <header>
            <NavigationBar setPage={props.setPage} user_id={userId}></NavigationBar>
        </header>
        <div className="SearchPage">
        <div className="movies-list">
            {props.datasearch.map((movie) => (
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
      </div>
    </div>
    ); 
}

export default Search; 