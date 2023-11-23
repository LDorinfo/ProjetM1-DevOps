
function Message(props){

    // ajouter des outils pour modifier ou supprimer le message si l'utilisateur est connecté. 

    //si je veux créer un bouton like pour un commentaire: 
    // il va falloir que je mette à jour les données du commentaire avec une requêtes fetch
    // il va falloir que j'ajoute un nombre dans la base de donnée = note. 

    
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
                <button>Like</button>
            }
		</li>
    )
}

export default Message;