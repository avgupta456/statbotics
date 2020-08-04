import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { Paper, Typography } from "@material-ui/core";

import { fetchTeam_Years, fetchTeamEvents_Team } from "./../../../api";
import { ReactTable, LineChart } from "./../../";

import styles from "./TeamView.module.css";

export default function TeamView() {
  const [eventData, setEventData] = useState([]);
  const [yearData, setYearData] = useState([]);
  const [chartData, setChartData] = useState({
    id: "",
    data: [{ x: 0, y: 0 }],
  });

  let { team } = useParams();
  const [name, setName] = useState([]);

  //column name, searchable, visible, link, hint
  const eventColumns = [
    ["Key", false, true, false, ""],
    ["Name", false, true, false, ""],
    ["Year", false, true, false, ""],
    ["Week", false, true, false, ""],
    ["Record", false, true, false, ""],
    ["Rank", false, true, false, ""],
    ["Elo", false, true, false, ""],
    ["OPR", false, true, false, ""],
  ];

  //column name, searchable, visible, link, hint
  const yearColumns = [
    ["Year", false, true, false, ""],
    ["Record", false, true, false, ""],
    ["Win Rate", false, true, false, ""],
    ["Max Elo", false, true, false, ""],
    ["Mean Elo", false, false, false, ""],
    ["Start Elo", false, false, false, ""],
    ["Pre Champs Elo", false, false, false, ""],
    ["End Elo", false, false, false, ""],
    ["Elo Rank", false, true, false, ""],
    ["Elo Percentile", false, true, false, ""],
    ["OPR", false, true, false, ""],
    ["Auto OPR", false, false, false, ""],
    ["Teleop OPR", false, false, false, ""],
    ["Endgame OPR", false, false, false, ""],
    ["ILS 1", false, false, false, ""],
    ["ILS 2", false, false, false, ""],
    ["OPR Rank", false, true, false, ""],
    ["OPR Percentile", false, true, false, ""],
  ];

  function cleanChart(team, data) {
    return {
      id: team,
      data: data.map(function (x, i) {
        return {
          x: x["year"],
          y: x["elo_max"],
        };
      }),
    };
  }

  function cleanYear(data) {
    const temp_data = data.reverse();
    return temp_data.map(function (x, i) {
      setName(x["name"]);

      let opr = parseInt(x["opr"] * 10) / 10;
      let opr_auto = -1;
      let opr_teleop = -1;
      let opr_endgame = -1;
      let ils_1 = -1;
      let ils_2 = -1;
      if (x["year"] >= 2016) {
        opr = parseInt(x["opr_no_fouls"] * 10) / 10;
        opr_auto = parseInt(x["opr_auto"] * 10) / 10;
        opr_teleop = parseInt(x["opr_teleop"] * 10) / 10;
        opr_endgame = parseInt(x["opr_endgame"] * 10) / 10;
        ils_1 = x["ils_1"];
        ils_2 = x["ils_2"];
      }
      return [
        x["year"],
        x["wins"] + "-" + x["losses"] + "-" + x["ties"],
        parseInt(x["winrate"] * 1000) / 10 + "%",
        x["elo_max"],
        x["elo_mean"],
        x["elo_start"],
        x["elo_pre_champs"],
        x["elo_end"],
        x["elo_rank"],
        Math.max(parseInt(x["elo_percentile"] * 1000) / 10, 0.1) + "%",
        opr,
        opr_auto,
        opr_teleop,
        opr_endgame,
        ils_1,
        ils_2,
        x["opr_rank"],
        Math.max(parseInt(x["opr_percentile"] * 1000) / 10, 0.1) + "%",
      ];
    });
  }

  function cleanEvent(data) {
    const temp_data = data.reverse();
    return temp_data.map(function (x, i) {
      let opr = x["opr"];
      if (x["year"] >= 2016) {
        opr = x["opr_no_fouls"];
      }
      return [
        x["event"],
        "events/" + x["event"] + "|" + x["event_name"],
        x["year"],
        x["week"],
        x["wins"] + "-" + x["losses"] + "-" + x["ties"],
        x["rank"],
        x["elo_max"],
        opr,
      ];
    });
  }

  useEffect(() => {
    const getTeamYears = async (team) => {
      const team_years = await fetchTeam_Years(team);
      setChartData(cleanChart(team, team_years));
      setYearData(cleanYear(team_years));
    };

    const getTeamEvents = async (team) => {
      const team_events = await fetchTeamEvents_Team(team);
      setEventData(cleanEvent(team_events));
    };

    getTeamYears(team);
    getTeamEvents(team);
  }, [team]);

  return (
    <Paper elevation={3} className={styles.body}>
      <Typography variant="h4">
        Team {team} - {name}
      </Typography>
      <ReactTable
        title={"Team " + team + ": Recent Events"}
        columns={eventColumns}
        data={eventData}
      />
      <br />
      <hr />
      <br />
      <ReactTable
        title={"Team " + team + ": Recent Years"}
        columns={yearColumns}
        data={yearData}
      />
      <br />
      <hr />
      <br />
      <Typography variant="h6">Team {team} - Elo through Time</Typography>
      <LineChart data={[chartData]} />
    </Paper>
  );
}
