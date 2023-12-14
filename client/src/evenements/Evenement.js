import './Evenement.css'; 
function Evenement(props){
    // affiche de l'evenement plus sa description dans une zone plutôt petite pour afficher plusieurs événement
    const handleClickPageEvenement= (event)=>{
        event.preventDefault(); 
        props.setPage(["event_page", props.dataevenement])
    }
    return( 
        <div>
            <div>
                <img className="imageEvenement" onClick={handleClickPageEvenement}>
                    src={props.dataevenement.image}
                    alt={props.dataevenement.title} 
                </img>
            </div>
            <div>
                <h4 className='titleEvent' onClick={handleClickPageEvenement}>{props.dataevenement.title}</h4>
                <p>{props.dataevenement.description}</p>
                {props.dataevenement.prix ==0? 
                    <p>Gratuit</p>
                :
                    <p>{props.dataevenement.prix} pour les membres</p>
                }   
            </div>
        </div>
    )
}

export default Evenement; 