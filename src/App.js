import React from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Nav, Navbar, NavItem } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

import { Routes } from './components'

import styles from './App.module.css'
import logo from "./static/favicon.ico";

const App = () => {
  return (
    <div>
      <Navbar>
        <Navbar.Brand href="/">
          <img
            alt="Logo"
            src={logo}
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{' '}
          Statbotics.io
        </Navbar.Brand>
        <Nav className="mr-auto">
          <LinkContainer className={styles.link} to="/">
            <NavItem>Home</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} to="/about">
            <NavItem>About</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} to="/teams">
            <NavItem>Teams</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} to="/years">
            <NavItem>Years</NavItem>
          </LinkContainer>
        </Nav>
      </Navbar>
      <Routes />
    </div>
  );
}

export default App;
