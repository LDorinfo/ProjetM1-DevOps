import { useState } from "react";
import "./Message.css";
import NoteStars from "./NoteStars";

function Message(props){
    const [like, setLike]= useState(props.dataMessage.like||0);
    const [isLiked, setIsLiked] = useState(props.dataMessage.like_user !== 0);
    const [isEditing, setIsEditing] = useState(false);
    const [editedText, setEditedText]= useState("");
    const [noteUser, setNoteUser]= useState(props.dataMessage.note); 
    // ajouter des outils pour modifier ou supprimer le message si l'utilisateur est connecté. 
    
    //si je veux créer un bouton like pour un commentaire: 
    // il va falloir que je mette à jour les données du commentaire avec une requêtes fetch
    // il va falloir que j'ajoute un nombre dans la base de donnée = note. 
    // mettre un useEffect pour obtenir le nombre de like dès qu'on charge la page. 
    const handleClickSetMessage = (evt)=>{
        evt.preventDefault();
        console.log(editedText);
        fetch(`http://localhost:5000/comments/editing`,{
            method: 'PUT',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comment_text : editedText, id_comment: props.dataMessage.id, noteUser : noteUser })
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Les modifications ont été envoyées");
            console.log(data); 
            setIsEditing(false);
            props.updateTextMessage();
        })
        .catch((error) => console.log(error));
    }

    const handleClickDelete = (evt)=>{
        evt.preventDefault();
        fetch(`http://localhost:5000/comments/delete`,{
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

    const handleClickLike =(evt)=>{
        evt.preventDefault(); 
        setIsLiked(!isLiked);
        fetch(`http://localhost:5000/comments/like`,{
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({id_comment: props.dataMessage.id })
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data); 
            setLike(data.like); 
        })
        .catch((error) => console.log(error));
    }
    return (
        <li className="le_msg">
            <h2>{props.dataMessage.username}</h2>
            <p>{props.dataMessage.comment_text}</p>
            {like}❤
			{props.user_id === props.dataMessage.user_id ? 
				<div>
                    {isEditing ? (
                        <div>
                        <NoteStars noteUser={noteUser} setNoteUser={setNoteUser} isClickable={true}/>
                        <textarea value={editedText} onChange={(evt) => setEditedText(evt.target.value)}/>
                        <button onClick={() => setIsEditing(!isEditing)}>Annuler</button>
                        <button onClick={handleClickSetMessage}>Envoyer</button>
                        </div>
                     ) : (
                        <div>
                        <NoteStars noteUser={noteUser} setNoteUser={setNoteUser} isClickable={false}/>
                        <button onClick={() => setIsEditing(!isEditing)}>Editer</button>
                        </div>
                    )}
                    <button onClick={handleClickDelete}>Supprimer</button>
                </div>
			:
            <div>
                <NoteStars noteUser={noteUser} setNoteUser={setNoteUser} isClickable={false}/>
                {isLiked? 
                    <button className="like-button" onClick={ handleClickLike }>
                     DisLike
                    </button>
                : 
                    <button className="like-button" onClick={ handleClickLike }>
                     Like
                    </button>
                }
                
            </div>
            }
		</li>
    )
}

export default Message;