import { useState,useEffect } from "react"; 
import NavDropdown from 'react-bootstrap/NavDropdown';


function ConnectionPanel(props){
    const [isconnected, setIsConnected] = useState(false);

    useEffect(() => {
		const fetchConnectedUsers = () => {
			fetch(`http://localhost:3001/api/users/connected`, {
			method: 'GET',
			credentials: 'include', // permet de stocker le cookie de session côté client
            body: JSON.stringify({id : props.isconnected})
			})
			.then(response => response.json()) //.json() convertit en JSON et retourne une promesse
			.then(data => {
				if (data.status === 200){
					setIsConnected(data.isconnected);
				}
			})
			.catch(error => console.log(error)); //si le fetch échoue (ex: serveur indisponible) on catch l'erreur
		};

		fetchConnectedUsers();
	},);

    const handleClickInscription= (evt)=>{
        evt.preventDefault()
		props.setPage(["signin_page", undefined])
    }

    const handleClickConnection= (evt)=>{
        evt.preventDefault()
		props.setPage(["login_page", undefined])
    }

    const handleClickProfil = (evt)=>{
        evt.preventDefault()
		props.setPage(["profil_page", props.isconnected])
        //permet de mettre l'id de l'utilisateur props.isconnected. 
        // Faut-il vérifier s'il y a un id plus tôt que de faire une requête au serveur. 
    }
    return(
        <NavDropdown title="Profil" id="collasible-nav-dropdown">
              {(isconnected) ? 
              <NavDropdown.Item onClick={handleClickProfil}>Profil</NavDropdown.Item>
              :
              <div>
              <NavDropdown.Item onClick={handleClickConnection}>Connection</NavDropdown.Item>
              <NavDropdown.Item onClick={handleClickInscription}>Inscription</NavDropdown.Item>
              </div>
              }
            </NavDropdown>
    )
}
export default ConnectionPanel; 