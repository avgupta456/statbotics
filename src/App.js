import React from 'react';

import { Route, Switch } from "react-router-dom";

import { Nav, Navbar } from "react-bootstrap";

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

import style from './App.module.css'
import logo from "./static/favicon.ico";

const App = () => {
  return (
    <div>
      <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
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
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav" className={style.collapse}>
        <Nav className="mr-auto">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="/about">About</Nav.Link>
          <Nav.Link href="/teams">Teams Table</Nav.Link>
          <Nav.Link href="/years">Years Table</Nav.Link>
          <Nav.Link href="/compare">Compare Teams</Nav.Link>
          <Nav.Link href="/predict">Predict Match</Nav.Link>
        </Nav>
      </Navbar.Collapse>
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
