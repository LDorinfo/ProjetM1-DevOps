import { useState} from "react";
import './BarreRecherche.css'


function BarreRecherche (props) {
	const [recherche,setRecherche] = useState("");
	
	const getRecheche= (evt) => {setRecherche(evt.target.value)};


	const handleClick = (evt) => {
		evt.preventDefault()
		let newerrorMessages = []
        //cette fonction fera la recherche, est ce qu'il faudrait utiliser query directement dans la requête: peut-être plus pour les filtres
        // Elle enverra une requête au serveur pour savoir. 
		fetch(`http://localhost:5000/search/search-multi?query=${recherche}`,{
			method:'GET', 
			credentials: 'include',
			headers: {"Content-Type": "application/json"},

		})
		.then(response => response.json()) // retourne une promesse
		.then(data => {
			console.log('Search successfully:', data);
        	props.setPage(["search_page", data])
            // réfléchir si ce n'est pas mieux de faire la recherche dans la search_page
			// ajouter l'id peut-être pour rester connecter ou trouver une solution avec les cookies
		  })
		.catch(error => {
			console.error('Error during search:', error);
			newerrorMessages.push("Une erreur c'est produite lors de la recherche.");
		  });
};

	return (
	<form className="search-bar">
        <input id="search_bar" type="text" placeholder="Chercher" onChange={getRecheche}/>
        <button className="submit_search_bar" onClick={handleClick}><img src="https://img.icons8.com/ios-filled/50/FFFFFF/search--v1.png" alt="search--v1"/></button>
    </form>);
};

export default BarreRecherche;
