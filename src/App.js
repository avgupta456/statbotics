import React, { useState, useEffect } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Nav, Navbar, NavItem } from "react-bootstrap";

import { LinkContainer } from "react-router-bootstrap";
import { Link } from "react-router-dom";

import { ReactTable } from './components'
import { fetchTeams } from './api';

import { Routes } from './components'

import styles from './App.module.css'
import logo from "./static/favicon.ico";

const App = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams.results);
    };

    fetchMyAPI();
  }, []);

  //column name, searchable
  const columns = [
    ["Number", true],
    ["Name", true],
    ["Current ELO", false],
    ["Recent ELO", false],
    ["Mean ELO", false],
    ["Max ELO", false],
  ];

  const data = teams.map(function(x){ return [
    x["team"],
    <a href={`teams/${x["team"]}`}>{x["name"]}</a>,
    x["elo"],
    x["elo_recent"],
    x["elo_mean"],
    x["elo_max"]
  ]});

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="#home">
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
          <Link to="/">Scratch</Link>
          <Link to="/">Scratch</Link>
          <Link to="/">Scratch</Link>
        </Nav>
        <Navbar.Collapse>
        <Nav pullRight>
          <LinkContainer to="/Home">
            <NavItem>Signup</NavItem>
          </LinkContainer>
          <LinkContainer to="/login">
            <NavItem>Login</NavItem>
          </LinkContainer>
        </Nav>
      </Navbar.Collapse>
      </Navbar>
      <ReactTable columns={columns} data={data}  className={styles.main}/>
      <Routes />
    </div>
  );
}

export default App;
