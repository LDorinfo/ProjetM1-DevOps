
import EvenementForm from "./EvenementForm";
import NavigationBar from "../NavigationBar";
import Evenement from "./Evenement";

function EvenementPage(props){
    return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
      <Evenement setPage={props.setPage} dataevenement={props.dataevenement}/>
      <EvenementForm change={props.dataevenement.idEvent}/>
    </div>
    )
}

export default EvenementPage; 