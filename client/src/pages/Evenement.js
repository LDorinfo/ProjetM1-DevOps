import ./Evenement.css; 
function Evenement(props){
    // affiche de l'evenement plus sa description dans une zone plutôt petite pour afficher plusieurs événement
    return( 
        <picture className="afficheEvent">
            <img className="image">
                src={props.dataevenement}
            </img>
        </picture>
    )
}

export default Evenement; 