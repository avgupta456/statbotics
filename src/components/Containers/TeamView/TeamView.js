import React, { useState, useEffect } from "react";
import  { useParams } from "react-router-dom";

import { Paper, Typography } from '@material-ui/core';

import { fetchTeam } from './../../../api'
import { LineChart } from './../../'

import styles from './TeamView.module.css'

export default function TeamView() {
  const [teamData, setTeamData] = useState({id:"", data:[{x:0, y:0}]})
  let { team } = useParams();

  function clean(team, data) {
    console.log(data)
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
      setTeamData(clean(team, new_teams));
    };

    getTeam(team)
  }, [team])

  return (
    <Paper elevation={3} className={styles.chart}>
      <Typography variant="h6">Team {team} - Elo through Time</Typography>
      <LineChart data={[teamData]} />
    </Paper>
  );
}
