import { useState } from "react";
import { FaPaperPlane } from 'react-icons/fa';
//permet de créer un message
function MessageForm(props){
    //const [dataMessage, setDataMessage]= useState(); not need
    const [text_comments, setTextComments]= useState(); 
    const [noteUser, setNoteUser]= useState(); 

    const getTextComments = (evt) => {setTextComments(evt.target.value)};
    const getNoteUser = (evt)=> {setNoteUser(evt.target.value)}

    const isValidForm = ()=>{
        let newerrorMessages = []
        if(text_comments.length === 0){
            newerrorMessages.push("Vous n'avez pas écrit de commentaire.");
            return false; 
        }
        if(props.username === undefined){
            newerrorMessages.push("Vous n'êtes pas connecté !");
            return false; 
        }
        if(props.idFilm === undefined){
            newerrorMessages.push("Etrange, cela ne devrait pas être possible");
            return false; 
        }
        return true; 
    }
    const handleClickSend = (evt)=>{
        let correctMessage = isValidForm(); 
        if(correctMessage){
            fetch(`http://localhost:5000/api/comments/create`,{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: props.username, idFilm: props.idFilm, note : noteUser, comments : text_comments  })
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                //setDataMessage(data); not need 
            })
            .catch((error) => console.log(error));
        }
    }

    return (
        <form className="formMessage">
			<label htmlFor="new_message_text">Nouveau message</label>
			<textarea id="new_message_text" value={text_comments} onChange={getTextComments}></textarea>
			<button className="buttonMSG" onClick={handleClickSend}><FaPaperPlane /> Envoyer</button>
		</form>
    )
}

export default MessageForm; 