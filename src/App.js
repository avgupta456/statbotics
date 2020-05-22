import React, { useState, useEffect } from 'react';
import { fetchTeams } from './api/index.js';
import { ReactTable } from './components'

const App = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams.results);
    };

    fetchMyAPI();
  }, []);

  console.log(teams);
  const data = teams.map(function(x){ return [x["team"], x["name"], x["elo"], x["elo_recent"], x["elo_mean"], x["elo_max"]] });

  return (
    <div>
    <ReactTable data={data}/>
    </div>
  );
}

export default App;
