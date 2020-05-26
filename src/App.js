import React from 'react';

import { Route, Switch } from "react-router-dom";

import { Nav, Navbar, NavItem } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

import {
  Home,
  Coming,
  TeamLookup,
  TeamYearLookup,
  TeamView,
  TeamCompare,
  Hypothetical,
}
from "./components/Containers";

import styles from './App.module.css'
import logo from "./static/favicon.ico";

const App = () => {
  return (
    <div>
      <Navbar bg="light">
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
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }} to="/">
            <NavItem>Home</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }}to="/about">
            <NavItem>About</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }} to="/teams">
            <NavItem>Teams Table</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }} to="/years">
            <NavItem>Years Table</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }} to="/compare">
            <NavItem>Compare Teams</NavItem>
          </LinkContainer>
          <LinkContainer className={styles.link} style={{ cursor: 'pointer' }} to="/predict">
            <NavItem>Predict Match</NavItem>
          </LinkContainer>
        </Nav>
      </Navbar>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/about">
          <Coming />
        </Route>
        <Route exact path="/teams">
          <TeamLookup />
        </Route>
        <Route exact path="/years">
          <TeamYearLookup />
        </Route>
        <Route path="/teams/:team">
         <TeamView />
        </Route>
        <Route path="/compare">
          <TeamCompare />
        </Route>
        <Route path="/predict">
          <Hypothetical />
        </Route>
      </Switch>
    </div>
  );
}


export default App;
