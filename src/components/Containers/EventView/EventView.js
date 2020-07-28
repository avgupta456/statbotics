import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { Paper, Typography } from "@material-ui/core";
import { Tabs, Tab } from "react-bootstrap";

import { ReactTable } from "./../../../components";

import { fetchEvent, fetchTeamEvents, fetchRankings } from "./../../../api";

import styles from "./EventView.module.css";

export default function EventView() {
  let { key } = useParams();

  const [event, setEvent] = useState("");
  const [year, setYear] = useState("");

  const [rankings, setRankings] = useState([]);
  const [rawData, setRawData] = useState([]);
  const [data, setData] = useState([]);

  //column name, searchable, visible, link, hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Rank", false, true, false, "Rank at Event"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    ["ILS 1", false, true, false, ""],
    ["ILS 2", false, true, false, ""],
  ];

  useEffect(() => {
    const getEvent = async (key) => {
      const event = await fetchEvent(key);
      setEvent(event["name"]);
      setYear(event["year"]);
    };

    const getTeamEvents = async (key) => {
      const team_events = await fetchTeamEvents(key, "-elo_end");
      setRawData(team_events);
    };

    const getRankings = async (key) => {
      const rankings = await fetchRankings(key);
      setRankings(rankings);
    };

    getEvent(key);
    getTeamEvents(key);
    getRankings(key);
  }, [key]);

  useEffect(() => {
    function clean(rawData, rankings) {
      let clean_data;
      if (year >= 2016) {
        clean_data = rawData.map(function (x, i) {
          return [
            x["team"],
            "./../teams/" + x["team"] + "|" + x["name"],
            rankings[x["team"]],
            x["elo_end"],
            parseInt(x["opr_no_fouls"] * 10) / 10,
            parseInt(x["opr_auto"] * 10) / 10,
            parseInt(x["opr_teleop"] * 10) / 10,
            parseInt(x["opr_endgame"] * 10) / 10,
            x["ils_1_end"],
            x["ils_2_end"],
          ];
        });
      } else {
        clean_data = rawData.map(function (x, i) {
          return [
            x["team"],
            "./../teams/" + x["team"] + "|" + x["name"],
            rankings[x["team"]],
            x["elo_end"],
            parseInt(x["opr_end"] * 10) / 10,
            -1,
            -1,
            -1,
            -1,
            -1,
          ];
        });
      }
      clean_data.sort((a, b) => a[2] - b[2]);
      return clean_data;
    }

    setData(clean(rawData, rankings));
  }, [year, rawData, rankings]);

  return (
    <Paper className={styles.body}>
      <h2>
        {year} {event}
      </h2>
      <br />
      <Tabs defaultActiveKey="insights" id="tab">
        <Tab eventKey="insights" title="Insights">
          <ReactTable
            title="Current Statistics"
            columns={columns}
            data={data}
          />
        </Tab>
        <Tab eventKey="simulation" title="Simulation">
          <Typography>Simulation</Typography>
        </Tab>
        <Tab eventKey="Test" title="Test">
          <Typography>Test</Typography>
        </Tab>
      </Tabs>
    </Paper>
  );
}
