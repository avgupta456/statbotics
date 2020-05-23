import React, { useState, useEffect } from "react";

import { ReactTable } from './../../../components';
import { fetchTeams } from './../../../api';

export default function TeamLookup() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchMyAPI = async () => {
      const new_teams = await fetchTeams();
      setTeams(new_teams.results);
    };

    fetchMyAPI();
  }, []);

  //column name, searchable, visible, filterable
  const columns = [
    ["Number", true, true, false],
    ["Name", true, true, false],
    ["Active", false, false, true],
    ["Current ELO", false, true, false],
    ["Recent ELO", false, true, false],
    ["Mean ELO", false, true, false],
    ["Max ELO", false, true, false],
  ];

  const data = teams.map(function(x){ return [
    x["team"],
    <a href={`teams/${x["team"]}`}>{x["name"]}</a>,
    (x["active"]?"active":"inactive"),
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
