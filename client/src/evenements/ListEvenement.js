import { useState, useEffect } from "react";
import Evenement from "./Evenement";

function ListEvenement(props){
    const [evenements, setEvenements]=useState([]); 
    // utilise une requête fetch pour obtenir tous les événements et 
    //les affiches graces au composant Evenement. 
    useEffect(()=>{
        const fetchEvenement = ()=>{
            fetch('http://localhost:5000/event/events', {
                method: 'GET',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
              })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data.events);

                    // Assurez-vous que data est un tableau avant de le définir comme état
                    if (Array.isArray(data.events)) {
                      setEvenements(data.events);
                    } else {
                      console.error("La réponse du serveur n'est pas un tableau.", data);
                    }
                })
                .catch((error) => console.log(error));
        }
        fetchEvenement(); 
    }, [setEvenements])


    return(
      <div className="card-container">
      {evenements.map((evenement) => (
        <Evenement setPage={props.setPage} dataevenement={evenement} key={evenement.id} />
      ))}
    </div>
    ); 
}

export default ListEvenement; 