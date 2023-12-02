//import { useState,useEffect } from "react"; 
import { NavDropdown, Nav } from 'react-bootstrap';
import '../NavigationBar.css';
import { useAuth } from "../AuthenticateContext";

function ConnectionPanel(props) {
    const {user}= useAuth();
    /**const [isconnected, setIsConnected] = useState();
  
    useEffect(() => {
      const fetchConnectedUsers = () => {
        fetch(`http://localhost:5000/api/users/connected?user_id=${props.isconnected}`, {
          method: 'GET',
          credentials: 'include',
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.isconnected) {
              setIsConnected(data.isconnected);
            }
            console.log(isconnected)
          })
          .catch((error) => console.log(error));
      };
  
      fetchConnectedUsers();
    }, []);
  */
    const handleClickInscription = (evt) => {
      evt.preventDefault();
      props.setPage(["signin_page", undefined]);
    };
  
    const handleClickConnection = (evt) => {
      evt.preventDefault();
      props.setPage(["login_page", undefined]);
    };
  
    const handleClickProfil = (evt) => {
      evt.preventDefault();
      props.setPage(["profil_page", user]);
    };

    const handleClickWatchlist = (evt) => {
      evt.preventDefault();
      props.setPage(["page_watchlist", user]);
    };

    const handleClickLogout = (evt) => {
      evt.preventDefault();
    
      fetch("http://localhost:5000/logout", {
        method: 'POST',
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
            <NavDropdown.Item onClick={handleClickProfil}>Profil</NavDropdown.Item>
            <NavDropdown.Item onClick={handleClickWatchlist}>Ma liste</NavDropdown.Item>
            <NavDropdown.Item onClick={handleClickLogout}>Se déconnecter</NavDropdown.Item>
          </NavDropdown>
        ) : (
          <div className="connection-links">
            <Nav.Link className="connection-link" onClick={handleClickConnection}>Connexion</Nav.Link>
            <Nav.Link className="connection-link" onClick={handleClickInscription}>Inscription</Nav.Link>
          </div>
        )}
      </div>
    );
  }
  
  export default ConnectionPanel;  