import { useState, useEffect } from "react";
import NavigationBar from "../NavigationBar.js";
import { useAuth } from "../AuthenticateContext.js";

function ProfilePage(props){
    const {user}= useAuth();
    const [userData, setUserData]= useState(""); 
    const [userEvents, setUserEvents] = useState([]);

    
    useEffect(()=>{
        const fetchUserData = () => {
            // Fetch popular movies
        fetch(`http://localhost:5000/users/userinfo?user_id=${user}`, {
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
        const fetchUserEvents= () => {
            fetch("http://localhost:5000/event/user_events", {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            setUserEvents(data.events);
        })
        .catch((error) => console.log(error));
    }
        fetchUserData(); 
        fetchUserEvents();
    }, [setUserData]); 

    // Des amis, une image de profil, les informations du profil
    // l'activité récente : commentaires, les coups de coeurs
    // gestion des notifications
    // modification des information de l'utilisateur. 
    const [isEditing, setIsEditing]= useState(false); 

    const [username, setUsername] = useState();
	const [firstName, setFirstName] = useState();

	const [lastName, setLastName] = useState();
	const [email, setEmail] = useState(); 
	const [phone_number, setPhone_number] = useState(); 
	const [pass1, setPass1] = useState("");

	const getUsername = (evt) => {setUsername(evt.target.value)};
	const getFirstName = (evt) => {setFirstName(evt.target.value)};
	const getLastName = (evt) => {setLastName(evt.target.value)};
	const getPass1 = (evt) => {setPass1(evt.target.value)};
	const getemail = (evt) => {setEmail(evt.target.value)};
	const getPhone_number = (evt) => {setPhone_number(evt.target.value);};

    const handleUpdateProfile = (evt) => {
        evt.preventDefault(); // lorsque l'on clique sur le bouton valider. 

        fetch('http://localhost:5000/users/modify', {
            method: 'PUT',
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



    return (
        <div>
            <NavigationBar setPage={props.setPage}></NavigationBar>
		<main>
			<section>
        <div >
            {!isEditing ? (
                <div>
                    <h2 className="centered-text">Profil de {userData.username}</h2>
                    <p>Email: {userData.email}</p>
                    <p>Nom: {userData.last_name}</p>
                    <p>Prénom: {userData.first_name}</p>
                    <p>Numéro de téléphone: {userData.phone_number}</p>
                    <button className="edit-button" onClick={() => setIsEditing(true)}>Modifier</button>                </div>
            ):(
                <div>
                <h2>Modifier ses informations</h2>
                <form className="profil_form">
					<label htmlFor="firstname">Nom</label><input id="firstname" placeholder="Nom" onChange={getFirstName} className="signin_input"/>
					<label htmlFor="lastname">Prénom</label><input id="lastname" placeholder="Prénom" onChange={getLastName} className="signin_input"/>
					<label htmlFor="signin_email">E-mail </label><input id="signin_email" placeholder="E-mail"  onChange={getemail} className="signin_input"/>
					<label htmlFor="signin_login">Nom d'utilisateur</label><input id="signin_login" placeholder="Nom d'utilisateur" onChange={getUsername} className="signin_input"/>
					<label htmlFor="signin_phone_number">Numéro de téléphone</label><input type="tel" id="signin_phoneNumber" placeholder="Numéro de téléphone" onChange={getPhone_number} className="signin_input"/>
					<label htmlFor="signin_mdp1">Mot de passe</label><input type="password" id="signin_mdp1" placeholder="Mot de passe" onChange={getPass1} className="signin_input"/>
					<button onClick={handleUpdateProfile}>Valider</button><button type="reset" onClick={()=>setIsEditing(false)}>Annuler</button>
				</form>
                </div>
            ) }
        </div >
        <div style={{ whiteSpace: 'nowrap' }}>
            {userEvents.map((event) => (
                <div key={event.id} style={{ display: 'inline-block', marginRight: '10px' }}>
                    {/* Display other event details as needed */}
                </div>
            ))}
        </div>
        </section>
        </main>
        </div>
    ); 
}

export default ProfilePage; 