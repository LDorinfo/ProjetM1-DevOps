import { useState, useEffect } from "react";
import {isValidEmail, isValidMdp, isValidNumber} from "../connexion/Signin.js"; 

function ProfilePage(props){
    const [userData, setUserData]= useState(""); 
    useEffect(()=>{
        const fetchUserData = () => {
            // Fetch popular movies
        fetch('http://localhost:5000/api/userinfo', {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            setUserData(data);
        })
        .catch((error) => console.log(error));
        }
        fetchUserData(); 
    }, [setUserData]); 

    // Des amis, une image de profil, les informations du profil
    // l'activité récente : commentaires, les coups de coeurs
    // gestion des notifications
    // modification des information de l'utilisateur. 
    const [isEditing, setIsEditing]= useState(false); 

    const [username, setUsername] = useState("");
	const [firstName, setFirstName] = useState("");

	const [lastName, setLastName] = useState("");
	const [email, setEmail] = useState(""); 
	const [phone_number, setPhone_number] = useState(""); 
	const [pass1, setPass1] = useState("");
	const [pass2, setPass2] = useState("");
    
	const getUsername = (evt) => {setUsername(evt.target.value)};
	const getFirstName = (evt) => {setFirstName(evt.target.value)};
	const getLastName = (evt) => {setLastName(evt.target.value)};
	const getPass1 = (evt) => {setPass1(evt.target.value)};
	const getPass2 = (evt) => {setPass2(evt.target.value)};
	const getemail = (evt) => {setEmail(evt.target.value)};
	const getPhone_number = (evt) => {setPhone_number(evt.target.value);};
	
    const handleUpdateProfile = (evt) => {
        evt.preventDefault(); // lorsque l'on clique sur le bouton valider. 

		let newerrorMessages = []
        if(!isValidEmail(email) || !isValidNumber(phone_number) || !isValidMdp(pass1) || 
        (username.length === 0 || pass1.length === 0 || pass2.length === 0 || firstName.length === 0 || lastName.length === 0 || phone_number.length === 0 || email.length ===0) 
        || (pass1 !== pass2 )){
            newerrorMessages.push("Erreur: il y a un problème dans l'un des champs");
        }else{
            fetch('http://localhost:5000/api/userinfo', {
                method: 'GET',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password : pass1, email: email, first_name: firstName, last_name: lastName, phone_number: phone_number})
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setUserData(data);
                setIsEditing(false);
            })
            .catch((error) => console.log(error));
        }
    }


    return (

        <div>
            {!isEditing ? (
                <div>
                    <h2>Profil de {userData.username}</h2>
                    <p>Email: {userData.email}</p>
                    <p>Nom: {userData.last_name}</p>
                    <p>Prénom: {userData.first_name}</p>
                    <p>Numéro de téléphone: {userData.phone_number}</p>
                    <button onClick={()=> setIsEditing(true)}>Modifier</button>
                </div>
            ):(
                <div>
                <form className="profil_form">
					<label htmlFor="firstname">Nom</label><input id="firstname" placeholder="Nom" onChange={getFirstName} className="signin_input"/>
					<label htmlFor="lastname">Prénom</label><input id="lastname" placeholder="Prénom" onChange={getLastName} className="signin_input"/>
					<label htmlFor="signin_email">E-mail </label><input id="signin_email" placeholder="E-mail"  onChange={getemail} className="signin_input"/>
					<label htmlFor="signin_login">Nom d'utilisateur</label><input id="signin_login" placeholder="Nom d'utilisateur" onChange={getUsername} className="signin_input"/>
					<label htmlFor="signin_phone_number">Numéro de téléphone</label><input type="tel" id="signin_phoneNumber" placeholder="Numéro de téléphone" onChange={getPhone_number} className="signin_input"/>
					<label htmlFor="signin_mdp1">Mot de passe</label><input type="password" id="signin_mdp1" placeholder="Mot de passe" onChange={getPass1} className="signin_input"/>
					<label htmlFor="signin_mdp2">Confirmation du mot de passe</label><input type="password" id="signin_mdp2" placeholder="Confirmation du mot de passe" onChange={getPass2} className="signin_input"/>
					<button onClick={handleUpdateProfile}>Valider</button><button type="reset">Réinitialiser</button>
				</form>
                </div>
            ) }
        </div>
    ); 
}

export default ProfilePage; 