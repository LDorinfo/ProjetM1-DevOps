
import { useState } from "react";

import { toast } from 'react-toastify';


function Signin (props) {
	const [login, setLogin] = useState("");
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [email, setEmail] = useState(""); 
	const [phone_number, setPhone_number] = useState(""); 

	const [errorMessages, setErrorMessages] = useState([]);

	const [pass1, setPass1] = useState("");
	const [pass2, setPass2] = useState("");


	const getLogin = (evt) => {setLogin(evt.target.value)};
	const getFirstName = (evt) => {setFirstName(evt.target.value)};
	const getLastName = (evt) => {setLastName(evt.target.value)};
	const getPass1 = (evt) => {setPass1(evt.target.value)};
	const getPass2 = (evt) => {setPass2(evt.target.value)};


	const getemail = (evt) => {setEmail(evt.target.value)}
	const getPhone_number = (evt) => {
		const newPhoneNumber = evt.target.value;
		setPhone_number(newPhoneNumber);
	}
	

	const isValidEmail = (email) => {
		const emailRes = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		// [^\s@]: permet d'avoir le début de l'email sans espace ni @
		return emailRes.test(email);
	  };
	
	const isValidNumber = (phone_number) => {
		const phoneRes = /^[0-9]{10}$/; 
		//Le numéro de téléphone doit avoir des nombres compris entre 0 et 9 et avoir 10 caractères
  		if(!phoneRes.test(phone_number)){
			toast.error("Le numéro de téléphone est invalide");
		} else {
			setErrorMessages([]);
		}
  	}

	const isValidMdp =  (password) =>{
		const passwordRes = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})/;
		// (?=.{8,}) permet de vérifier si le mot de passe à 8 caractères ou plus
		// (?=.*[!@#$%^&*]) permet de vérifier si le mot de passe contient un caractère spéciale 
		//(?=.*[A-Z]) permet de vérifier que le mot de passe contient au moins une majuscule. 

		if (!passwordRes.test(password)) {
			toast.error("Le mot de passe doit avoir au moins 8 caractères, une majuscule et un caractère spécial.");
			return false;
		} else {
			setErrorMessages([]);
			return true;
		}
	}

	const submissionHandler = (evt) => {
		evt.preventDefault()

		isValidNumber(phone_number);

		let newerrorMessages = []
		// Vérifie si tous les champs sont bien remplis
		let signinOK = true; //variable supplémentaire nécessaire car useState maj de façon asynchrone

		if (login.length === 0 || pass1.length === 0 || pass2.length === 0 || firstName.length === 0 || lastName.length === 0 || phone_number.length === 0 || email.length ===0)
		{
			newerrorMessages.push("Veuillez remplir tous les champs");
			signinOK = false;
		}
		// Vérifie si les 2 mdp sont bien les mêmes
		if (pass1 !== pass2 ){
			newerrorMessages.push("Erreur: mots de passe différents");
			signinOK = false;
		}
		if(!isValidMdp(pass1)){
			newerrorMessages.push("Invalide mot");
			signinOK= false; 
		}
		if( !isValidEmail(email)){
			newerrorMessages.push("Veillez entrer un email valide");
			signinOK = false; 
		}

		// si l'inscription de l'utilisateur est vrai
		if(signinOK == true){
			console.log("true"); 
			// on doit envoyer les données au serveur
			fetch('http://localhost:5000/register',{
				method:'POST', 
				headers: {"Content-Type": "application/json"},
				credentials: 'include',//afin d'être conforme avec la politique du CORS
				body: JSON.stringify({username : login, password : pass1, last_name : lastName, first_name :firstName, phone_number, email })
			})
			.then(response => response.json()) // retourne une promesse
			.then(data => {
				// Handle the response data as needed
				console.log('User registered successfully:', data);
				props.setPage(["home_page", data.id])
				// You can perform additional actions, such as redirecting the user or displaying a success message.
			  })
			.catch(error => {
				console.error('Error during registration:', error);
				newerrorMessages.push("Une erreur s'est produite lors de l'inscription. Veuillez réessayer.");
			  });
		}
		else
			setErrorMessages(newerrorMessages);
	}

	const onClick = (evt)=>{
		evt.preventDefault()
		props.setPage(["login_page", undefined])
	}
	
	return (
		<div className="signin_div">
			<h1 className="signin_h1">Inscription</h1>
			<form className="signin_form">
				<label htmlFor="firstname">FirstName</label><input id="firstname" onChange={getFirstName} className="signin_input"/>
				<label htmlFor="lastname">LastName</label><input id="lastname" onChange={getLastName} className="signin_input"/>
				<label htmlFor="signin_login">Login</label><input id="signin_login" onChange={getLogin} className="signin_input"/>
				<label htmlFor="signin_mdp1">Password</label><input type="password" id="signin_mdp1" onChange={getPass1} className="signin_input"/>
				<label htmlFor="signin_mdp2">Password (2)</label><input type="password" id="signin_mdp2" onChange={getPass2} className="signin_input"/>
				<label htmlFor="signin_email">Email </label><input id="signin_email" onChange={getemail} className="signin_input"/>
				<label htmlFor="signin_phone_number">Phone Number</label><input type="tel" id="signin_phoneNumber" onChange={getPhone_number} className="signin_input"/>
				<button onClick={submissionHandler}>S'inscrire</button><button type="reset">Réinitialiser</button>
				<button onClick={onClick}>Login</button>
			</form>
			{errorMessages.map((message,i) => <p style={{color:"red"}} key={i}>{message}</p>)}
		</div>
	)
}
//<button onClick={onClick}>Login</button>


export default Signin;
