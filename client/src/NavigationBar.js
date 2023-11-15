
import Container from 'react-bootstrap/Container';
import { useState } from 'react';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import ConnectionPanel from './ConnectionPanel';
import BarreRecherche from './BarreRecherche';
import Logo from './Logo.js'; 

function NavigationBar(props) {

  
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Logo />
        <Navbar.Brand href="#home">CineVerse</Navbar.Brand>
        <BarreRecherche setPage={props.setPage} user_id={props.user_id} />
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">

            <Nav.Link href="#actualité">Actualité</Nav.Link>
            <ConnectionPanel isconnected={props.user_id} setPage={props.setPage}/>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavigationBar ;