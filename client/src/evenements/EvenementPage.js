import { useAuth } from "../AuthenticateContext";
import EvenementForm from "./EvenementForm";
import NavigationBar from "../NavigationBar";
import Evenement from "./Evenement";

function EvenementPage(props){
  const {user}= useAuth();

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
      <EvenementForm change={props.data.id}/>
    </div>
  )
}

export default EvenementPage; 