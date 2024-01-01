import './Evenement.css'; 
function Evenement(props){
    // affiche de l'evenement plus sa description dans une zone plutôt petite pour afficher plusieurs événement
    const handleClickPageEvenement= (event)=>{
        event.preventDefault(); 
        props.setPage(["event_page", props.dataevenement])
    }
    return( 
        <div className="card" onClick={handleClickPageEvenement}>
      <img className="imageEvenement" src={props.dataevenement.image} alt={props.dataevenement.title} />
      <div>
        <h4 className="titleEvent">{props.dataevenement.title}</h4>
        <p className="description">{props.dataevenement.description}</p>
        {props.dataevenement.prix === 0 ? (
          <p className="prix">Gratuit</p>
        ) : (
          <p className="prix">{props.dataevenement.prix} Pour les membres</p>
        )}
      </div>
    </div>
  );
}

export default Evenement; 