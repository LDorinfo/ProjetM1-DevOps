
import EvenementForm from "./EvenementForm";
import NavigationBar from "../NavigationBar";
import Evenement from "./Evenement";

function EvenementPage(props){
    return (
    <div>
      <header>
        <NavigationBar setPage={props.setPage}/>
      </header>
      <Evenement setPage={props.setPage} dataevenement={props.data}/>
      <EvenementForm change={props.data.id}/>
    </div>
    )
}

export default EvenementPage; 