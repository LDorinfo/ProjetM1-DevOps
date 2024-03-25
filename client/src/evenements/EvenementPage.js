import React, { useState, useEffect } from 'react';
import { useAuth } from "../AuthenticateContext";
import NavigationBar from "../NavigationBar";
import Evenement from "./Evenement";
import EvenementForm from "./EvenementForm";
import './Evenement.css'; 
import { toast } from 'react-toastify';


function EvenementPage(props){
  const {user}= useAuth();
  const [eventusername, setEventUsername] = useState('');
  const [isparticipant, setParticipant] = useState(false);
  useEffect(() => {
    console.log(props.data)
    const fetchUsername = () => {
      fetch(`http://localhost:5000/users/userinfo?user_id=${props.data.user_id}`, {
          method: 'GET',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' }
      })
      .then((response) => response.json())
      .then((data) => {
        setEventUsername(data.username);
      })
      .catch((error) => console.log(error));
    };
    const fetchParticipantStatus = () => {
      fetch(`http://localhost:5000/event/isparticipant?user_id=${user}&evenement_id=${props.data.id}`, {
          method: 'GET',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' }
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setParticipant(data.participant);
      })
      .catch((error) => console.log(error));
    };

    fetchUsername();
    fetchParticipantStatus();
  }, [props.data.user_id]);

  const handleClickAddParticipant = (evt)=>{
      evt.preventDefault();
      fetch(`http://localhost:5000/event/adduser`,{
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user : user , evenement_id: props.data.id})
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => console.log(error));
      
  }

  const handleClickDeleteParticipant = (evt)=>{
    evt.preventDefault();
    fetch(`http://localhost:5000/event/deleteuser`,{
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user : user , evenement_id: props.data.id})
    })
    .then((response) => response.json())
    .then((data) => {
      toast(data.message);
    })
    .catch((error) => console.log(error));
    
  }
  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
      <div className="event-container">
        <Evenement setPage={props.setPage} dataevenement={props.data}/> 
        {props.data.user_id == user ? <p>Vous êtes l'organisateur</p> : 
        <div>
          {isparticipant ?
          <button className='buttonparticiper' onClick={handleClickDeleteParticipant}>Se désincrire</button>
          :
          <button className='buttonparticiper' onClick={handleClickAddParticipant}>Participer</button>
          }
        </div>
        }
        <h2>Modifier l'évenement</h2>
        {props.data.user_id == user ? <EvenementForm change={props.data.id}/> : <p>Créateur : {eventusername}</p>}
      </div>
    </div>
  )
}

export default EvenementPage; 