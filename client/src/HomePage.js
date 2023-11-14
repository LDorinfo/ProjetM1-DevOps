import { useState, useEffect } from "react";

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
		<div>
			<h1>CineVerse</h1>
		<main>
			
		</main>
		</div>
	);
}

export default HomePage;