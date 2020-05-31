import React from "react";
import { useHistory } from "react-router-dom";

import { Nav, Navbar, NavDropdown } from "react-bootstrap";

import { TeamSelect } from "./.."

import styles from "./Navigation.module.css";
import logo from "./../../static/favicon.ico";

export default function Navigation() {
  const history = useHistory();

  const routeChange = (team) => {
    history.push(`/teams/${team.value}`);
  }

  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
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
      <Navbar.Collapse id="responsive-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link className={styles.navItem} href="/">Home</Nav.Link>
        <Nav.Link className={styles.navItem} href="/teams">Teams Table</Nav.Link>
        <Nav.Link className={styles.navItem} href="/years">Years Table</Nav.Link>
        <Nav.Link className={styles.navItem} href="/compare">Compare Teams</Nav.Link>
        <Nav.Link className={styles.navItem} href="/predict">Predict Match</Nav.Link>
      </Nav>
      <NavDropdown.Divider />
      <Nav>
        <TeamSelect
        className={styles.search}
        onChange={routeChange}
        isMulti={false}
        />
      </Nav>
    </Navbar.Collapse>
    </Navbar>
  );
}
