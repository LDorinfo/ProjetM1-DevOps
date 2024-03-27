import React,{ useState } from "react";
import { useAuth } from "../AuthenticateContext";
import { FaPaperPlane } from 'react-icons/fa';
import {toast} from 'react-toastify';
import './EvenementForm.css'; 
import SelecteurDate from "../SelecteurDate";
import { format, parse, startOfWeek, getDay, parseISO} from 'date-fns';

function EvenementForm(props){
    const {user}= useAuth();
    const [textEvent, setTextEvent] = useState(""); 
    const [prix, setPrix]= useState(0); 
    const [title, setTitle]= useState(""); 
    const [startdate, setDateStart]= useState(''); 
    const [enddate, setDateEnd]= useState(''); 
    const [nbmax, setNbmax]= useState(0);
    console.log(user)
    const getTitleEvent= (event)=>{
        setTitle(event.target.value); 
    }
    const getPrix = (event)=>{
        setPrix(event.target.value); 
    }
    const getMaxParticipants= (event)=> {
      setNbmax(event.target.value);
    }
    // ajouter une affiche 

    const [file, setFile]=useState("");
    const handleFileChange = (event) => {
      setFile(event.target.value); 
		/*const selectfile= event.target.files[0];
        if (selectfile) {
            const reader = new FileReader();
            reader.onloadend = () => {
              console.log("Image lue avec succès !");
              setImagePreview(reader.result);
            };
            reader.readAsDataURL(selectfile);
          } else {
            setImagePreview(null);
          }*/
	};

    const getTextEvent = (evt) => {setTextEvent(evt.target.value)};
    //const getNoteUser = (evt)=> {setNoteUser(evt.target.value)}
    // plus besoin

    //ajouter une date 
    const handleChangeStart = (e) =>{
      const formattedDate = format(new Date(e.target.value), "yyyy, M, d, H, m");
      setDateStart(formattedDate);
    }
    const handleChangeEnd = (e) =>{
      const formattedDate = format(new Date(e.target.value), "yyyy, M, d, H, m");
      setDateEnd(formattedDate);
    }
    const isValidForm = ()=>{
      console.log(user)
      console.log(title)
      console.log(textEvent)
      console.log(prix)
      console.log(file)
        if(textEvent.length === 0){
            toast.error("Vous n'avez pas écrit de commentaire.");
            return false; 
        }
        if(!user){
            console.log(user);
            toast.error("Vous n'êtes pas connecté !");
            return false; 
        }
        return true; 
    }
    const handleClickSend = (evt)=>{ 
        evt.preventDefault();
        
        if(isValidForm()){
            fetch(`http://localhost:5000/event/create`,{
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: user, enddate : enddate, nbmax: nbmax, startdate: startdate, image: file, title : title, prix : prix, description : textEvent  })
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setFile(""); 
                setTitle(""); 
                setPrix(0); 
                setTextEvent("");  
                fetch(`http://localhost:5000/event/adduser`,{
                  method: 'PUT',
                  credentials: 'include',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ user : user , evenement_id: data.id})
                })
                .then((response) => response.json())
                .then((data) => {
                  console.log(data);
                })
                .catch((error) => console.log(error));
            })
            .catch((error) => console.log(error));
        }
    }

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
              body: JSON.stringify({ user_id: user, nbmax: nbmax, enddate : enddate, startdate : startdate, idEvent : props.change, file : file, title : title, prix : prix, description : textEvent  })
          })
          .then((response) => response.json())
          .then((data) => {
              console.log(data);
              setFile(""); 
              setTitle(""); 
              setPrix(""); 
              setTextEvent("");  
              //if(props.onEventUpdate){
              //  props.onEventUpdate();
              //}
          })
          .catch((error) => console.log(error));
      }
  }

//<input type="file" id="event_picture" onChange={handleFileChange} />
return (
  <form className="formEvent">
    <div className="labelandarea">
      <div>
        <label htmlFor="title_event">Title</label>
        <input
          id="title_event"
          placeholder="Title"
          onChange={getTitleEvent}
          className="event_title_input"
        />
        <label htmlFor="end_date">Date de debut</label>
        <SelecteurDate handleChange={handleChangeStart} date={startdate} />
        <label htmlFor="end_date">Date de fin</label>
        <SelecteurDate handleChange={handleChangeEnd} date={enddate} />
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
      <label htmlFor="event_picture" className="event_picture_label">
          Ajouter une affiche (URL ou téléchargement)
        </label>
        <input
          type="text"
          placeholder="URL de l'image"
          value={file}
          onChange={handleFileChange}
        />
        <div>
          <label htmlFor="max_personnes">Nombre maximum de participants</label>
          <input
              id="max_personnes"
              type="number" /* Utilisez le type "number" pour restreindre les entrées aux nombres */
              placeholder="0"
              onChange={getMaxParticipants}
              className="event_maxparticipants_input"
          />
        </div>
            <button
      className="buttonEvent"
      onClick={props.change !== undefined ? handleClickSendChange : handleClickSend}
    >
      <FaPaperPlane /> Envoyer
    </button>
    </div>
    <div className="change_affiche">
        {file && (
          <img
            src={file}
            alt="Aperçu de l'image"
            className="image-preview"
          />
        )}
    
    </div>
  </form>
);
}

export default EvenementForm;