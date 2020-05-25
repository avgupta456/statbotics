import React, { useState, useEffect } from "react";

import { Jumbotron } from "react-bootstrap";

import { fetchTeam } from './../../../api'
import { LineChart } from './../../'

import styles from './TeamView.module.css'

export default function TeamView() {
  const [teamData, setTeamData] = useState({id:"", data:[{x:0, y:0}]})

  function clean(team, data) {
    return {
      id: team,
      data: data.map(
        function(x, i) {
          return {
            x: x["year"],
            y: x["elo_max"],
          }
        }
      )
    }
  };

  useEffect(() => {
    const getTeam = async (team) => {
      const new_teams = await fetchTeam(team);
      setTeamData(clean(team, new_teams.results));
    };

    getTeam(254)
  }, [])

  return (
    <Jumbotron className={styles.height}>
      <LineChart data={[teamData]} />
    </Jumbotron>
  );
}
