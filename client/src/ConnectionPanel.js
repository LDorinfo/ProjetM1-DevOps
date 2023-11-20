import { useState,useEffect } from "react"; 
import { NavDropdown, Nav } from 'react-bootstrap';
import './NavigationBar.css';

function ConnectionPanel(props) {
    const [isconnected, setIsConnected] = useState();
  
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
      props.setPage(["profil_page", props.isconnected]);
    };
  
    return (
      <div>
        {isconnected ? (
          <NavDropdown title="Profil" id="collasible-nav-dropdown">
            <NavDropdown.Item onClick={handleClickProfil}>Profil</NavDropdown.Item>
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