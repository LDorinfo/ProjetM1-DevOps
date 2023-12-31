import { useState } from "react";
import { FaPaperPlane } from 'react-icons/fa';
import "./Message.css";
import "./NoteStars.css";
import NoteStars from "./NoteStars";

//permet de créer un message
function MessageForm(props){
    //const [dataMessage, setDataMessage]= useState(); not need
    const [text_comments, setTextComments]= useState(); 
    const [noteUser, setNoteUser]= useState(0); 

    const getTextComments = (evt) => {setTextComments(evt.target.value)};
    //const getNoteUser = (evt)=> {setNoteUser(evt.target.value)}
    // plus besoin

    const isValidForm = ()=>{
        if(text_comments.length === 0){
            console.error("Vous n'avez pas écrit de commentaire.");
            return false; 
        }
        if(props.username === null){
            console.log(props.username);
            console.error("Vous n'êtes pas connecté !");
            return false; 
        }
        if(props.idFilm === undefined){
            console.error("Etrange, cela ne devrait pas être possible");
            return false; 
        }
        return true; 
    }
    const handleClickSend = (evt)=>{ 
        evt.preventDefault();
        if(isValidForm()){
            fetch(`http://localhost:5000/comments/create`,{
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: props.username, idFilm: props.idFilm.id, note : noteUser, comments : text_comments  })
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                //setDataMessage(data); not need 
                props.updateMessage(data); 
                setTextComments(''); 
            })
            .catch((error) => console.log(error));
        }
    }

    return (
        <form className="formMessage">
            <div className="labelandarea">
			<label htmlFor="new_message_text">Nouveau commentaire</label>
			<textarea id="new_message_text" placeholder="Nouveau commentaire..." value={text_comments} onChange={getTextComments}></textarea>
            </div>
            <NoteStars noteUser={noteUser} setNoteUser={setNoteUser} isClickable={true}/>
			<button className="buttonMSG" onClick={handleClickSend}><FaPaperPlane /> Envoyer</button>
		</form>
    )
}

export default MessageForm; 