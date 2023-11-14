import { useState} from "react";
import { FaSearch } from 'react-icons/fa';

function BarreRecherche (props) {
	const [recherche,setRecherche] = useState("");
	
	const getRecheche= (evt) => {setRecherche(evt.target.value)};

	const handleClickSearch = (evt) => {
		evt.preventDefault()
        if(props.isconnected){
            props.setPage(["search_page", props.user_id]);
        }
        else{
            props.setPage(["search_page", undefined])
        }
	}

	const handleClick = (evt) => {
		evt.preventDefault()
		let newerrorMessages = []
        // cette fonction permettra de savoir si l'utilisateur est dans la base de données
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
        <input id="search_bar" type="text" onChange={handleClickSearch}/>
        <button className="submit_search_bar" onClick={handleClick}><FaSearch/>Recherche</button>
    </form>);
};

export default BarreRecherche;
