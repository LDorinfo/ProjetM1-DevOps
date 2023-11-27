import { useState } from "react";
import "./Message.css";

function Message(props){
    const [like, setLike]= useState(0);
    const [isEditing, setIsEditing] = useState(false);
    const [editedText, setEditedText]= useState("");
    // ajouter des outils pour modifier ou supprimer le message si l'utilisateur est connecté. 
    
    //si je veux créer un bouton like pour un commentaire: 
    // il va falloir que je mette à jour les données du commentaire avec une requêtes fetch
    // il va falloir que j'ajoute un nombre dans la base de donnée = note. 
    const  handleClick = (evt)=>{
        evt.preventDefault();
        setLike(like+1);
    }
    // mettre un useEffect pour obtenir le nombre de like dès qu'on charge la page. 
    const handleClickSetMessage = (evt)=>{
        evt.preventDefault();
        console.log(editedText);
        fetch(`http://localhost:5000/api/comments/editing`,{
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comment_text : editedText, id_comment: props.dataMessage.id})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Les modifications ont été envoyées");
            console.log(data); 
            setIsEditing(false);
        })
        .catch((error) => console.log(error));
    }

    const handleClickDelete = (evt)=>{
        evt.preventDefault();
        fetch(`http://localhost:5000/api/comments/delete`,{
            method: 'DELETE',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({id_comment: props.dataMessage.id})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Les modifications ont été envoyées");
            console.log(data); 
            props.updateMessage(data.id)
        })
        .catch((error) => console.log(error));
    }
    return (
        <li className="le_msg">
            <h2>{props.dataMessage.username}</h2>
            <p>{props.dataMessage.note}</p>
            <p>{props.dataMessage.comment_text}</p>
			{props.user_id === props.dataMessage.user_id ? 
				<div>
                    {isEditing ? (
                        <div>
                        <textarea value={editedText} onChange={(evt) => setEditedText(evt.target.value)}/>
                        <button onClick={() => setIsEditing(!isEditing)}>Annuler</button>
                        <button onClick={handleClickSetMessage}>Envoyer</button>
                        </div>
                     ) : (
                        <div>
                        <button onClick={() => setIsEditing(!isEditing)}>Editer</button>
                        </div>
                    )}
                    <button onClick={handleClickDelete}>Supprimer</button>
                </div>
			:
            <div>
                <button className="like-button" onClick={ handleClick }>
                    Like
                </button>
            </div>
            }
		</li>
    )
}

export default Message;