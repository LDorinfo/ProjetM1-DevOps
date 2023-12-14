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
                  console.log(data);
                  setEvenements(data || []);
                })
                .catch((error) => console.log(error));
        }
        fetchEvenement(); 
    }, [setEvenements])


    return(
        <div>
        {evenements.map((evenement) => (
            <Evenement setPage={props.setPage} dataevenement={evenement} />
        ))}
        </div>
    ); 
}

export default ListEvenement; 