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

  return (
    <div>
      <ReactTable teams={teams}/>
    </div>
  );
}

export default App;
