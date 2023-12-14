import React, { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import ConnectionPanel from './connexion/ConnectionPanel';
import BarreRecherche from './search/BarreRecherche';
import './NavigationBar.css';

function NavigationBar(props) {
  const [filmsDropdownOpen, setFilmsDropdownOpen] = useState(false);
  const [serieDropdownOpen, setSerieDropdownOpen] = useState(false);


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
        props.setPage(["search_page", data])
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
      props.setPage(["search_page", data]) 
    })
    .catch((error)=> console.log(error))
  }

  return (
    <Navbar collapseOnSelect expand="lg" variant="dark">
      <Container>
        <img className="popcorn-icon" src="https://img.icons8.com/fluency/48/popcorn.png" alt="popcorn"/>
        <Navbar.Brand href="./Homepage.js">CineVerse</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href='./Homepage.js'>Accueil</Nav.Link>
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
              <NavDropdown.Item href='#'onClick={()=>handleClickTV(14)}>Fantastique</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickTV(878)}>Science-Fiction</NavDropdown.Item>
              <NavDropdown.Item href='#' onClick={()=>handleClickTV(27)}>Horror</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <BarreRecherche setPage={props.setPage} />
            <ConnectionPanel setPage={props.setPage} />
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavigationBar;
