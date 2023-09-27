import { useState} from "react";
import MainPage from "./MainPage";
import { toast } from 'react-toastify';
import "./Login.css"

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
        // cette fonction permettra de savoir si l'utilisateur est dans la base de données
        // Elle enverra une requête au serveur pour savoir. 
        toast("Connexion!");
        props.setPage(["home_page", setLogin])
       

	};

	return (
		<form className="form_login">
			<h1 className="Connection_log">Connexion</h1>
			<label htmlFor="login">Login</label><input id="login_log" onChange={getLogin}/>
			<label htmlFor="mdp">Mot de passe</label><input type="password" id="mdp_log" onChange={getPassword}/>
			<button type="submit" onClick={handleClick} className="button_log">Se connecter</button>
			<button className="link-button" onClick={handleClickSignin}>Inscription</button>
		</form>
	);
};

export default Login;