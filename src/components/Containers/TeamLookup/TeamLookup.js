import React, { useState, useEffect } from "react";

import Paper from '@material-ui/core/Paper';

import { ReactTable } from './../../../components';
import { fetchTeams } from './../../../api';
import styles from './TeamLookup.module.css';

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
    ["District", false, false, false],
    ["Region", false, false, false],
    ["Current ELO", false, true, false],
    ["Recent ELO", false, true, false],
    ["Mean ELO", false, true, false],
    ["Max ELO", false, true, false],
  ];

  const data = teams.map(function(x, i){ return [
    x["team"],
    <a href={`teams/${x["team"]}`}>{x["name"]}</a>,
    (x["active"]?"Active":"Inactive"),
    x["district"],
    x["region"],
    x["elo"],
    x["elo_recent"],
    x["elo_mean"],
    x["elo_max"],
  ]});

  const title = "Team Lookup"

  return (
    <div>
      <Paper
        elevation={3}
        className = {styles.body}

        children = {
          <ReactTable title={title} columns={columns} data={data}/>
        }
      />
    </div>
  );
}
