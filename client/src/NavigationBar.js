import React, { useState, useEffect } from 'react';
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
/**  const [user_id, setUserId] = useState(); 
  useEffect(() => {
    // permet de factoriser le code afin d'éviter de se balader un attribut. 
    const fetchIsconnected = ()=>{
      fetch(`http://localhost:5000/@me`, {
          headers: {"Content-Type": "application/json"}
        }
      )
      .then((response)=> response.json())
      .then((data)=>{
        // s'il y a des données dans la response.
        console.log(data)
        setUserId(data.id); // Initialize with an empty array if results are undefined
      })
      .catch((error)=> console.log(error))
  };
  fetchIsconnected();

}, []);
*/
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
              <NavDropdown.Item href='#'>Action</NavDropdown.Item>
              <NavDropdown.Item href='#'>Comédie</NavDropdown.Item>
              <NavDropdown.Item href='#'>Drame</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown 
              title="Série Tv" 
              id="serie-dropdown" 
              show={serieDropdownOpen} 
              onMouseEnter={() => setSerieDropdownOpen(true)} 
              onMouseLeave={() => setSerieDropdownOpen(false)}
            >
              {/* Add TV series categories as NavDropdown items */}
              <NavDropdown.Item href='#'>Drame</NavDropdown.Item>
              <NavDropdown.Item href='#'>Science-Fiction</NavDropdown.Item>
              <NavDropdown.Item href='#'>Comédie</NavDropdown.Item>
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
