import { useEffect, useState } from "react";
import NavigationBar from "../NavigationBar";
import MessageForm from "../commentaire/MessageForm.js"; 
import Message from "../commentaire/Message.js";

function PageFilm(props){
    // obtenir les informations sur les commentaires du films. 
    // obtenir les statistiques du nombre de personne qui a consulté cette page. 
    // modification de la base de données. 

    const [comments, setComments]= useState([]); 
    
    useEffect(() => {
        const fetchComments = () => {
          // requête pour avoir les commentaires concernant ce films.
        fetch(`http://localhost:5000/api/comments?idFilm=${props.dataFilm[0].id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        .then((response) => response.json())
        .then((data) => {
            if(data.status == "Not found Id in database Comment"){
                setComments([]);
            }
            else{
                console.log(data);
                setComments(data);
            }
        })
        .catch((error) => console.log(error));
        }
    fetchComments();

    }, [props.dataFilm]);

    return (<div>
        <header>
            <NavigationBar setPage={props.setPage} ></NavigationBar>
        </header>
        <main>
			<aside>
				<ul>
					Statistics
				</ul>
			</aside>
			<section>
			<div id="new_message">
				<MessageForm username={props.dataFilm[1]} idFilm={props.dataFilm[0].id} />
			</div>
			<article>
				<h1 className="titreMessage" >Messages</h1>
                {comments.map(message=>(
                    <Message dataMessage={message} user_id={props.dataFilm[1]}/>
                ))}
			</article>
			</section>
		</main>
    </div>)
}

export default PageFilm; 