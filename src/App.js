import React, { useState, useEffect } from 'react';
import { fetchTeams, fetchTeam } from './api/index.js';

import { ReactTable } from './components'

const App = () => {
  const [teams, setTeams] = useState([]);
  const [team, setTeam] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams.results);
    };

    fetchMyAPI();
  }, []);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_team = await fetchTeam();
      setTeam(new_team.results);
    };

    fetchMyAPI();
  }, []);

  console.log(teams);
  console.log(team)

  return (
    <div>
      <ReactTable teams={teams}/>
    </div>
  );
}

export default App;
