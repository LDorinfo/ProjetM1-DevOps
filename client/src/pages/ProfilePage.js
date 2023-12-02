import { useState, useEffect } from "react";

function ProfilePage(props){
    const [userData, setUserData]= useState(); 
    console.log("hello");
    useEffect(()=>{
        const fetchUserData = () => {
            // Fetch popular movies
        fetch('http://localhost:5000/api/userinfo', {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
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
    // information de l'utilisateur. 
    return (
        <div>
            {userData ? (
                <div>
                    <h2>Profil de {userData.username}</h2>
                    <p>Email: {userData.email}</p>
                    <p>Nom: {userData.last_name}</p>
                    <p>Prénom: {userData.first_name}</p>
                    <p>Numéro de téléphone: {userData.phone_number}</p>
                </div>
            ):(
                <p>Chargement...</p>
            ) }
        </div>
    ); 
}

export default ProfilePage; 