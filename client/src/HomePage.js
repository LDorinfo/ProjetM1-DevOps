import { useState, useEffect } from "react";
import './HomePage.css'
import NavigationBar from "./NavigationBar";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

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
				<NavigationBar setPage={props.setPage}></NavigationBar>
		</header>

			<main>
			<Card style={{ width: '18rem' }}>
				<Card.Img variant="top" src="./public/Narnia.jpg/100px180" />
				<Card.Body>
					<Card.Title>Narnia</Card.Title>
					<Card.Text>
					Une armoire magique qui s'ouvre sur un autre monde. 
					Cela va être automatisé dans un composant qui appelera la base de données pour chaque film. 
					</Card.Text>
					<Button variant="primary">En savoir plus</Button>
				</Card.Body>
    		</Card>
			</main>
		</body>
	);
}

export default HomePage;