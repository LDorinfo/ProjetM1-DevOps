import { useState} from "react";
import MainPage from "./MainPage";

import { toast } from 'react-toastify';


import { useState } from "react";
import "./Signin.css"
import { toast } from 'react-toastify';


function Signin (props) {
	const [login, setLogin] = useState("");
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");

	const [errorMessages, setErrorMessages] = useState([]);

	const [pass1, setPass1] = useState("");
	const [pass2, setPass2] = useState("");
	const getLogin = (evt) => {setLogin(evt.target.value)};
	const getFirstName = (evt) => {setFirstName(evt.target.value)};
	const getLastName = (evt) => {setLastName(evt.target.value)};
	const getPass1 = (evt) => {setPass1(evt.target.value)};
	const getPass2 = (evt) => {setPass2(evt.target.value)};

	const submissionHandler = (evt) => {
		evt.preventDefault()
		let newerrorMessages = []
		// Vérifie si tous les champs sont bien remplis
		let signinOK = true; //variable supplémentaire nécessaire car useState maj de façon asynchrone

		if (login.length === 0 || pass1.length === 0 || pass2.length === 0 || firstName.length === 0 || lastName.length === 0)
		{
			newerrorMessages.push("Veuillez remplir tous les champs");
			signinOK = false
		}
		// Vérifie si les 2 mdp sont bien les mêmes
		if (pass1 !== pass2){
			newerrorMessages.push("Erreur: mots de passe différents");
			signinOK = false
		}

		
		else
			setErrorMessages(newerrorMessages);
	}

	return (
		<div className="signin_div">
			<h1 className="signin_h1">Inscription</h1>
			<form className="signin_form">
				<label htmlFor="firstname">Prénom</label><input id="firstname" onChange={getFirstName} className="signin_input"/>
				<label htmlFor="lastname">Nom</label><input id="lastname" onChange={getLastName} className="signin_input"/>
				<label htmlFor="signin_login">Login</label><input id="signin_login" onChange={getLogin} className="signin_input"/>
				<label htmlFor="signin_mdp1">Mot de passe</label><input type="password" id="signin_mdp1" onChange={getPass1} className="signin_input"/>
				<label htmlFor="signin_mdp2">Mot de passe (2)</label><input type="password" id="signin_mdp2" onChange={getPass2} className="signin_input"/>
				<button onClick={submissionHandler}>S'inscrire</button><button type="reset">Réinitialiser</button>
			</form>
			{errorMessages.map((message,i) => <p style={{color:"red"}} key={i}>{message}</p>)}
		</div>
	)
}



export default Signin;