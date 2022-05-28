import React, { useEffect } from "react";

import { Typography } from "@material-ui/core";
import { Card } from "react-bootstrap";

import { fetchTeam_Years } from "./../../../api";
import { LineChart, TeamSelect } from "./../../";

import styles from "./TeamCompare.module.css";

export default function TeamCompare() {
  const [chosenTeams, setChosenTeams] = React.useState([]);
  const [teamsData, setTeamsData] = React.useState([
    { id: "", data: [{ x: 0, y: 0 }] },
  ]);

  function clean(team, data) {
    return {
      id: team,
      data: data.map(function (x, i) {
        return { x: x["year"], y: x["elo_max"] };
      }),
    };
  }

  useEffect(() => {
    const getTeamsData = async (teams) => {
      var new_teams = [];
      for (var i = 0; i < teams.length; i++) {
        const team = teams[i].value.substring(6);
        const teamData = await fetchTeam_Years(team);
        new_teams.push(clean(team, teamData));
      }
      setTeamsData(new_teams);
    };

    getTeamsData(chosenTeams);
  }, [chosenTeams]);

  function teamsClick(teams) {
    if (teams === null) {
      setChosenTeams([]);
    } else {
      setChosenTeams(teams);
    }
  }

  return (
    <Card className={styles.chart}>
      <TeamSelect
        className={styles.dropdown}
        onChange={teamsClick}
        isMulti={true}
        includeEvents={false}
      />
      <div className={styles.height}></div>
      <Typography variant="h6">Team Comparison - Elo through Time</Typography>
      <LineChart data={teamsData} />
    </Card>
  );
}
