import { useState} from "react";
import { toast } from 'react-toastify';
import "./Login.css"
import Button from 'react-bootstrap/Button';


function Login (props) {
	const [login,setLogin] = useState("");
	const [password,setPassword] = useState("");

	const getLogin = (evt) => {setLogin(evt.target.value)};
	const getPassword = (evt) => {setPassword(evt.target.value)};

	const handleClickSignin = (evt) => {
		evt.preventDefault()
		props.setPage(["signin_page", undefined])
	}

	const handleClick = (evt) => {
		evt.preventDefault()
		let newerrorMessages = []
        // cette fonction permettra de savoir si l'utilisateur est dans la base de données
        // Elle enverra une requête au serveur pour savoir. 
		fetch('http://localhost:5000/login',{
			method:'POST', 
			headers: {"Content-Type": "application/json"},
			credentials: 'include',
			body: JSON.stringify({username : login, password})

		})
		.then(response => response.json()) // retourne une promesse
		.then(data => {
			// Handle the response data as needed
			console.log('User connected successfully:', data);
			toast("Connexion!");
        	props.setPage(["home_page", data.id])
			// You can perform additional actions, such as redirecting the user or displaying a success message.
		  })
		.catch(error => {
			console.error('Error during connexion:', error);
			newerrorMessages.push("Une erreur s'est produite lors de la connection. Veuillez réessayer.");
		  });
};

	return (
		<form className="form_login">
			<h1 className="Connection_log">Connexion</h1>
			<label htmlFor="login">Login</label><input id="login_log" onChange={getLogin}/>
			<label htmlFor="mdp">Mot de passe</label><input type="password" id="mdp_log" onChange={getPassword}/>
			<Button type="submit" onClick={handleClick} className="button_log" variant="primary">Se connecter</Button>{' '}
			<Button className="link-button" onClick={handleClickSignin} variant="secondary">Inscription</Button>
		</form>
	);
};

export default Login;
