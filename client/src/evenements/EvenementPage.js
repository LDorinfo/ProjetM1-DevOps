import React, { useState, useEffect } from 'react';
import { useAuth } from "../AuthenticateContext";
import NavigationBar from "../NavigationBar";
import Evenement from "./Evenement";
import EvenementForm from "./EvenementForm";

function EvenementPage(props){
  const {user}= useAuth();
  const [eventusername, setEventUsername] = useState('');

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

    fetchUsername();
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
  return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
      <Evenement setPage={props.setPage} dataevenement={props.data}/>
      
      <button onClick={handleClickAddParticipant}>Participer</button>
      {props.data.user_id == user ? <EvenementForm change={props.data.id}/> : <p>Créateur : {eventusername}</p>}
    </div>
  )
}

export default EvenementPage; 