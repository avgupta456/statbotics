import React, { useState, useEffect } from 'react';
import { fetchTeams } from './api/index.js';

const App = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams);
    };

    fetchMyAPI();
  }, []);

  console.log(teams);

  return (
    <div>
      <h1>Teams in Database:</h1>
      {teams.map((team, i) => <h2 key={i}>{team.number} {team.name}</h2>)}
    </div>
  );
}

export default App;
