import { useState, useEffect } from "react";
import './HomePage.css'
import BarreRecherche from "./BarreRecherche";

function HomePage (props) {
	const [connectedUsers, setConnectedUsers] = useState([]);

	useEffect(() => {
		const fetchConnectedUsers = () => {
			fetch(`http://localhost:3001/api/users/connected`, {
			method: 'GET',
			credentials: 'include', // permet de stocker le cookie de session côté client
            body: JSON.stringify({id : props.user_id})
			})
			.then(response => response.json()) //.json() convertit en JSON et retourne une promesse
			.then(data => {
				if (data.status === 200){
					setConnectedUsers(data.isconnected);
				}
			})
			.catch(error => console.log(error)); //si le fetch échoue (ex: serveur indisponible) on catch l'erreur
		};

		fetchConnectedUsers();
	  },);

	return (
		<body>
		<header>
				<h1>CineVerse</h1>
				//barre de navigation
				<div class="NavBar_container">
					//logo 
					//créer un composant pour que toutes les pages aient le logo
					<BarreRecherche></BarreRecherche>
					//mettre un composant permettant soit d'afficher le profil soit de mettre un lien vers la page login et inscription
					
				</div>
		</header>

			<main>
			</main>
		</body>
	);
}

export default HomePage;