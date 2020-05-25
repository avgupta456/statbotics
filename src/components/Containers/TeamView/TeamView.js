import React, { useState, useEffect } from "react";

import { Jumbotron } from "react-bootstrap";

import { fetchTeam } from './../../../api'
import { LineChart } from './../../'

import styles from './TeamView.module.css'

export default function TeamView() {
  const [teamData, setTeamData] = useState([])

  function clean(data) {
    console.log(data)
    const new_data = data.map(function(x, i){ return {
      x: x["year"],
      y: x["elo_max"],
    }});
    console.log(new_data)
    return new_data
  };

  useEffect(() => {
    const getTeam = async (team) => {
      const new_teams = await fetchTeam(team);
      setTeamData(clean(new_teams.results));
    };

    getTeam(254)
  }, [])

  console.log(teamData)
  const newTeamData = [{data: teamData, id: "254"}]
  console.log(newTeamData)

  return (
    <Jumbotron className={styles.height}>
      <LineChart data={newTeamData} />
    </Jumbotron>
  );
}
