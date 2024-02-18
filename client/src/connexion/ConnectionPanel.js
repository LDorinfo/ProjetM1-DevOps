import React, {useEffect} from 'react';
import { NavDropdown, Nav, NavLink } from 'react-bootstrap';
import { Link } from 'react-router-dom'; // Importer Link pour la navigation
import '../NavigationBar.css';
import { useAuth } from "../AuthenticateContext";

function ConnectionPanel() {
    const { user } = useAuth();

    const handleClickLogout = (evt) => {
        evt.preventDefault();
        fetch("http://localhost:5000/users/logout", {
            method: 'PUT',
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                // Handle success, e.g., redirect to the login page
                console.log(data.message);
                window.location.reload();
            })
            .catch((error) => console.log(error));
    };
    return (
        <div>
            {user ? (
                <NavDropdown title="Profil" id="collasible-nav-dropdown">
                    {/* Ajouter l'ID de l'utilisateur comme paramètre dans les liens */}
                    <NavDropdown.Item as={Link} to={`/profile/${user}`}>Profil</NavDropdown.Item>
                    <NavDropdown.Item as={Link} to={`/watchlist/${user}`}>Ma liste</NavDropdown.Item>
                    <NavDropdown.Item as={Link} to="/planning">Mon planning</NavDropdown.Item>
                    <NavDropdown.Item onClick={handleClickLogout}>Se déconnecter</NavDropdown.Item>
                </NavDropdown>
            ) : (
                <div className="connection-links">
                    {/* Utiliser NavLink pour la navigation */}
                    <NavLink as={Link} to="/login" className="connection-link">Connexion</NavLink>
                    <NavLink as={Link} to="/signin" className="connection-link">Inscription</NavLink>
                </div>
            )}
        </div>
    );
}

export default ConnectionPanel;
