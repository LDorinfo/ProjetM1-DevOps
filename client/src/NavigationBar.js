import React, { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import ConnectionPanel from './ConnectionPanel';
import BarreRecherche from './BarreRecherche';
import './NavigationBar.css';

function NavigationBar(props) {
  const [filmsDropdownOpen, setFilmsDropdownOpen] = useState(false);
  const [serieDropdownOpen, setSerieDropdownOpen] = useState(false);

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
            <BarreRecherche setPage={props.setPage} user_id={props.user_id} />
            <ConnectionPanel isconnected={props.user_id} setPage={props.setPage} />
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavigationBar;
