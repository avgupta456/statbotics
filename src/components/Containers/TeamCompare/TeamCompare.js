import React, {useEffect, useState} from "react";

import { Paper, Typography } from '@material-ui/core';
import WindowedSelect from "react-windowed-select";

import { fetchTeams, fetchTeam } from './../../../api'
import { LineChart } from './../../'

import styles from './TeamCompare.module.css'

export default function TeamCompare() {
  const [teams, setTeams] = React.useState([])
  const [chosenTeams, setChosenTeams] = React.useState([])
  const [teamsData, setTeamsData] = React.useState([{id:"", data:[{x:0, y:0}]}])

  function cleanList(teams) {
    return (
      teams.map(
        function(x, i) {
          return x["team"]
        }
      )
    )
  }

  function clean(team, data) {
    console.log(data)
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
    const getTeams = async () => {
      const new_teams = await fetchTeams(true);
      setTeams(cleanList(new_teams.results))
    }

    const getTeamsData = async (teams) => {
      var new_teams = []
      for(var i=0;i<teams.length;i++) {
        const team = teams[i].value;
          console.log(team)
        const teamData = await fetchTeam(team);
        new_teams.push(clean(team, teamData.results))
      }
      setTeamsData(new_teams)
    }

    if(teams.length===0) {
      getTeams()
    }

    getTeamsData(chosenTeams)

  }, [teams, chosenTeams])

  function teamsClick(teams) {
    setChosenTeams(teams)
  }

  return (
    <Paper elevation={3} className={styles.chart}>
      {console.log(teams)}
      <WindowedSelect
        className={styles.dropdown}
        isMulti = {true}
        onChange = {teamsClick}
        options={teams.map(function(x) {return({value: x, label: x})})}
      />;
      <Typography variant="h6">Team Comparison - ELO through Time</Typography>
      <LineChart data={teamsData} />
    </Paper>
  );
}
