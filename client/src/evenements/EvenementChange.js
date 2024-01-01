import React,{ useState } from "react";
import { useAuth } from "../AuthenticateContext";
import { FaPaperPlane } from 'react-icons/fa';
import {toast} from 'react-toastify';

function EvenementChange(props){
    const {user}= useAuth();
    const [textEvent, setTextEvent] = useState(""); 
    const [prix, setPrix]= useState(0); 
    const [title, setTitle]= useState(""); 
    console.log(user)
    const getTitleEvent= (event)=>{
        setTitle(event.target.value); 
    }
    const getPrix = (event)=>{
        setPrix(event.target.value); 
    }
    // ajouter une affiche 

    const [file, setFile]=useState("");
    const handleFileChange = (event) => {
      setFile(event.target.value); 
	};

    const getTextEvent = (evt) => {setTextEvent(evt.target.value)};

    const handleClickSendChange = (evt)=>{ 
        evt.preventDefault();
        if(!user){
            console.log(user);
            toast.error("Vous n'êtes pas connecté !");
            return false; 
        }else{
            fetch(`http://localhost:5000/event/change`,{
                method: 'PUT',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: user,idEvent : props.change, file : file, title : title, prix : prix, description : textEvent  })
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                //setFile(""); 
                //setTitle(""); 
                //setPrix(""); 
                //setTextEvent("");  
            })
            .catch((error) => console.log(error));
        }
    }

//<input type="file" id="event_picture" onChange={handleFileChange} />
  return (
    <form className="formEvent">
      <div className="labelandarea">
        <label htmlFor="title_event">Title</label>
        <input
          id="title_event"
          placeholder="Title"
          onChange={getTitleEvent}
          className="event_title_input"
        />
        <div className="change_affiche">
          <label htmlFor="event_picture" className="event_picture_label">
            Ajouter une affiche (URL ou téléchargement)
          </label>
        <input
            type="text"
            placeholder="URL de l'image"
            value={file}
            onChange={handleFileChange}
        />
          {file && (
            <img
              src={file}
              alt="Aperçu de l'image"
              className="image-preview"
            />
          )}
        </div>
        <label htmlFor="new_description_text">Description</label>
        <textarea
          id="new_description_text"
          placeholder="Description..."
          value={textEvent}
          onChange={getTextEvent}
        ></textarea>
      </div>
      <label htmlFor="prix_title">Prix</label>
        <input
          id="prix_event"
          placeholder="0"
          onChange={getPrix}
          className="event_prix_input"
        />
      <button className="buttonEvent" onClick={props.change !== undefined ? handleClickSendChange :  handleClickSend}>
        <FaPaperPlane /> Envoyer
      </button>
    </form>
  );
}

export default EvenementChange;