import { useState} from "react";
import { FaSearch } from 'react-icons/fa';
import Button from 'react-bootstrap/Button';

function BarreRecherche (props) {
	const [recherche,setRecherche] = useState("");
	
	const getRecheche= (evt) => {setRecherche(evt.target.value)};


	const handleClick = (evt) => {
		evt.preventDefault()
		let newerrorMessages = []
        //cette fonction fera la recherche, est ce qu'il faudrait utiliser query directement dans la requête: peut-être plus pour les filtres
        // Elle enverra une requête au serveur pour savoir. 
		fetch('http://localhost:5000/api/search-multi',{
			method:'GET', 
			headers: {"Content-Type": "application/json"},
			credentials: 'include',
			body: JSON.stringify({query : recherche})

		})
		.then(response => response.json()) // retourne une promesse
		.then(data => {
			console.log('Search successfully:', data);
        	props.setPage(["search_page", data])
            // réfléchir si ce n'est pas mieux de faire la recherche dans la search_page
			// ajouter l'id peut-être pour rester connecter ou trouver une solution avec les cookies
		  })
		.catch(error => {
			console.error('Error during connexion:', error);
			newerrorMessages.push("Une erreur s'est produite lors de la connection. Veuillez réessayer.");
		  });
};

	return (
	<form>
        <label htmlFor="search_bar">Rechercher</label>
        <input id="search_bar" type="text" onChange={getRecheche}/>
        <Button className="submit_search_bar" onClick={handleClick}><FaSearch/>Recherche</Button>
    </form>);
};

export default BarreRecherche;
