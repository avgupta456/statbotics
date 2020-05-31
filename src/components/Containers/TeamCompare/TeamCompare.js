import React, {useEffect} from "react";

import { Typography } from '@material-ui/core';
import { Card } from 'react-bootstrap'

import { fetchTeam } from './../../../api'
import { LineChart, TeamSelect } from './../../'

import styles from './TeamCompare.module.css'

export default function TeamCompare() {
  const [chosenTeams, setChosenTeams] = React.useState([])
  const [teamsData, setTeamsData] = React.useState([{id:"", data:[{x:0, y:0}]}])

  function clean(team, data) {
    return {
      id: team,
      data: data.map(
        function(x, i) {
          return {x: x["year"], y: x["elo_max"]}
        }
      )
    }
  }

  useEffect(() => {
    const getTeamsData = async (teams) => {
      var new_teams = []
      for(var i=0;i<teams.length;i++) {
        const team = teams[i].value;
        const teamData = await fetchTeam(team, "elo_recent");
        new_teams.push(clean(team, teamData.results))
      }
      setTeamsData(new_teams)
    }

    getTeamsData(chosenTeams)

  }, [chosenTeams, teamsData])

  function teamsClick(teams) {
    if(teams===null) {setChosenTeams([])}
    else {setChosenTeams(teams)}
  }

  return (
    <Card className={styles.chart}>
      <TeamSelect
        className={styles.dropdown}
        onChange={teamsClick}
        isMulti={true}
      />
      <div className={styles.height}></div>
      <Typography variant="h6">Team Comparison - Elo through Time</Typography>
      <LineChart data={teamsData} />
    </Card>
  );
}
