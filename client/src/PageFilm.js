import { useEffect, useState } from "react";
import NavigationBar from "./NavigationBar";

function PageFilm(props){
    // obtenir les informations sur les commentaires du films. 
    // obtenir les statistiques du nombre de personne qui a consulté cette page. 
    // modification de la base de données. 

    const [comments, setComments]= useState([]); 
    console.log(props.dataFilm); 
    useEffect(() => {
        const fetchComments = () => {
          // requête pour avoir les commentaires concernant ce films.
        fetch(`http://localhost:5000/api/comments?idFilm=${props.dataFilm.id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            setComments(data || []);
        })
        .catch((error) => console.log(error));
        }
    fetchComments();

    }, [props.dataFilm]);

    return (<div>
        <header>
            <NavigationBar setPage={props.setPage} ></NavigationBar>
        </header>
    </div>)
}

export default PageFilm; 