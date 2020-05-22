import React, { useState, useEffect } from 'react';
import { fetchTeams } from './api/index.js';
import { ReactTable } from './components'
import styles from './App.module.css'

const App = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams.results);
    };

    fetchMyAPI();
  }, []);

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
    <div className={styles.main}>
      <ReactTable columns={columns} data={data}/>
    </div>
  );
}

export default App;
