import React, { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import ConnectionPanel from './connexion/ConnectionPanel';
import BarreRecherche from './search/BarreRecherche';
import './NavigationBar.css';
import Cinemamaps from './pages/Cinemamaps';
import { useNavigate,Route } from 'react-router-dom';

function NavigationBar(props) {
  const [filmsDropdownOpen, setFilmsDropdownOpen] = useState(false);
  const [serieDropdownOpen, setSerieDropdownOpen] = useState(false);
  const history = useNavigate();

  const handleClickMovies = (indice) => {
    // perme de faire la recherche pour les films dans les filtres sélectionnées. 
      fetch(`http://localhost:5000/search/filtre?query=${indice}`, {
          method: 'GET',
          headers: {"Content-Type": "application/json"}, 
          credentials: 'include'
        }
      )
      .then((response)=> response.json())
      .then((data)=>{
        console.log(data);
        history(`/search?query=${indice}&data=${JSON.stringify(data)}`);
      })
      .catch((error)=> console.log(error))
}
const handleClickTV = (indice) => {
  // perme de faire la recherche pour les films dans les filtres sélectionnées. 
    fetch(`http://localhost:5000/search/tv/filtre?query=${indice}`, {
        method: 'GET',
        headers: {"Content-Type": "application/json"}, 
        credentials: 'include'
      }
    )
    .then((response)=> response.json())
    .then((data)=>{
      console.log(data);
      history(`/search?query=${indice}&data=${JSON.stringify(data)}`);
    })
    .catch((error)=> console.log(error))
  }

  const handleClickMaps = () => {
    // Naviguer vers la page de cinéma
    history("/maps");
  };

  return (
    <Navbar collapseOnSelect expand="lg" variant="dark">
      <Container>
        <img className="popcorn-icon" src="https://img.icons8.com/fluency/48/popcorn.png" alt="popcorn"/>
        <Navbar.Brand href="/">CineVerse</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href='/'>Accueil</Nav.Link>
            <NavDropdown 
              title="Films" 
              id="films-dropdown" 
              show={filmsDropdownOpen} 
              onMouseEnter={() => setFilmsDropdownOpen(true)} 
              onMouseLeave={() => setFilmsDropdownOpen(false)}
              className="custom-dropdown"
            >
              {/* Add film categories as NavDropdown items */}
              <NavDropdown.Item href='#' onClick={()=>handleClickMovies(28)}>Action</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickMovies(35)}>Comédie</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickMovies(18)}>Drame</NavDropdown.Item>
              <NavDropdown.Item href='#'onClick={()=>handleClickMovies(14)}>Fantastique</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickMovies(878)}>Science-Fiction</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickMovies(27)}>Horror</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown 
              title="Série Tv" 
              id="serie-dropdown" 
              show={serieDropdownOpen} 
              onMouseEnter={() => setSerieDropdownOpen(true)} 
              onMouseLeave={() => setSerieDropdownOpen(false)}
            >
              {/* Add TV series categories as NavDropdown items */}
              <NavDropdown.Item href='#'onClick={()=>handleClickTV(10765)}>Fantastique</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickTV(10751)}>Family</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickTV(10759)}>Action & Adventure</NavDropdown.Item>
            </NavDropdown>
            <Nav.Link href='./maps' onClick={handleClickMaps}>Cinéma</Nav.Link>
          </Nav>
          <Nav>
            <BarreRecherche />
            <ConnectionPanel />
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavigationBar;
