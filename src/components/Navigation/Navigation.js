import React from "react";
import { useHistory } from "react-router-dom";

import { Nav, Navbar, NavDropdown } from "react-bootstrap";

import { TeamSelect } from "./..";

import styles from "./Navigation.module.css";
import logo from "./../../static/favicon.ico";

export default function Navigation() {
  const [navExpanded, setNavExpanded] = React.useState(false);
  const history = useHistory();

  const routeChange = (team) => {
    history.push(`${team.value}`);
    setNavExpanded(false);
  };

  return (
    <Navbar expanded={navExpanded} expand="xl" bg="dark" variant="dark">
      <Navbar.Brand href="/">
        <img
          alt="Logo"
          src={logo}
          width="30"
          height="30"
          className="d-inline-block align-top"
        />{" "}
        Statbotics.io
      </Navbar.Brand>
      <Navbar.Toggle
        onClick={() => setNavExpanded(!navExpanded)}
        aria-controls="responsive-navbar-nav"
      />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/"
          >
            Home
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/teams"
          >
            Teams
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/years"
          >
            Years
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/events"
          >
            Events
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/compare"
          >
            Compare Teams
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/predict"
          >
            Predict Match
          </Nav.Link>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/docs"
          >
            Docs
          </Nav.Link>
        </Nav>
        <NavDropdown.Divider />
        <Nav>
          <TeamSelect
            className={styles.search}
            onChange={routeChange}
            isMulti={false}
            includeEvents={true}
          />
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}
