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

  const columns = [
    {
      label: "Number",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      label: "Name",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      label: "ELO",
      options: {
        filter: false,
        sort: true,
        searchable: false,
      }
    },
    {
      label: "ELO Recent",
      options: {
        filter: false,
        sort: true,
        searchable: false,
      }
    },
    {
      label: "ELO Mean",
      options: {
        filter: false,
        sort: true,
        searchable: false,
      }
    },
    {
      label: "ELO Max",
      options: {
        filter: false,
        sort: true,
        searchable: false,
      }
    },
  ]

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
    <ReactTable columns={columns} data={data}/>
    </div>
  );
}

export default App;
