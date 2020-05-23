import React, { useState, useEffect } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

import { ReactTable } from './components'
import { fetchTeams } from './api';

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
          <Nav.Link href="#home">Lookup</Nav.Link>
          <Nav.Link href="#features">Tables</Nav.Link>
          <Nav.Link href="#pricing">About</Nav.Link>
        </Nav>
      </Navbar>
      <ReactTable columns={columns} data={data}  className={styles.main}/>
    </div>
  );
}

export default App;
