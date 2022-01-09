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
    <Navbar expanded={navExpanded} expand="md" bg="dark" variant="dark">
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
            href="/teams"
          >
            Teams
          </Nav.Link>
          <NavDropdown title="Historical">
            <Nav.Link
              onClick={() => setNavExpanded(false)}
              className={styles.dropdown}
              href="/all/teams"
            >
              Teams
            </Nav.Link>
            <Nav.Link
              onClick={() => setNavExpanded(false)}
              className={styles.dropdown}
              href="/all/team-years"
            >
              Team Years
            </Nav.Link>
            <Nav.Link
              onClick={() => setNavExpanded(false)}
              className={styles.dropdown}
              href="/all/events"
            >
              Events
            </Nav.Link>
          </NavDropdown>
          <Nav.Link
            onClick={() => setNavExpanded(false)}
            className={styles.navItem}
            href="/docs"
          >
            API Docs
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
