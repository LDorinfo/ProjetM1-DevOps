import { useState } from "react";

function Message(props){
    const [like, setLike]= useState();
    // ajouter des outils pour modifier ou supprimer le message si l'utilisateur est connecté. 

    //si je veux créer un bouton like pour un commentaire: 
    // il va falloir que je mette à jour les données du commentaire avec une requêtes fetch
    // il va falloir que j'ajoute un nombre dans la base de donnée = note. 
    const  handleClick = (evt)=>{
        console.log("ok");
    }
    // mettre un useEffect pour obtenir le nombre de like dès qu'on charge la page. 
    
    return (
        <li className="le_msg">
            <h1>{props.dataMessage.user_id}</h1>
            <p>{props.dataMessage.text_comments}</p>
            <p>{props.dataMessage.note}</p>
			{props.user_id === props.dataMessage.user_id ? 
				<div>
                    <button>Editer</button>
                    <button>Supprimer</button>
                </div>
			:
                <button className="like-button" onClick={ handleClick }>
                <span className="likes-counter">{ `Like | ${like}` }</span>
                </button>
            }
		</li>
    )
}

export default Message;