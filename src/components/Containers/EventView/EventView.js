import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { Paper, Typography } from "@material-ui/core";
import { Tabs, Tab } from "react-bootstrap";

import { ReactTable } from "./../../../components";

import { fetchEvent, fetchTeamEvents } from "./../../../api";

import styles from "./EventView.module.css";

export default function EventView() {
  let { key } = useParams();

  const [event, setEvent] = useState("");
  const [teamEvents, setTeamEvents] = useState([]);

  //column name, searchable, visible, link, hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    ["ILS 1", false, true, false, ""],
    ["ILS 2", false, true, false, ""],
  ];

  useEffect(() => {
    function clean(team_events) {
      return team_events.map(function (x, i) {
        getTeamName(x["team"]);
        return [
          x["team"],
          "teams/" + x["team"] + "|" + x["name"],
          x["elo_end"],
          parseInt(x["opr_no_fouls"] * 10) / 10,
          parseInt(x["opr_auto"] * 10) / 10,
          parseInt(x["opr_teleop"] * 10) / 10,
          parseInt(x["opr_endgame"] * 10) / 10,
          x["ils_1_end"],
          x["ils_2_end"],
        ];
      });
    }

    const getEvent = async (key) => {
      const event = await fetchEvent(key);
      setEvent(event["name"]);
    };

    const getTeamEvents = async (key) => {
      const team_events = await fetchTeamEvents(key);
      setTeamEvents(clean(team_events));
    };

    getEvent(key);
    getTeamEvents(key);
  }, [key]);

  return (
    <Paper className={styles.body}>
      <h2>{event}</h2>
      <br />
      <Tabs defaultActiveKey="insights" id="tab">
        <Tab eventKey="insights" title="Insights">
          <Typography>Insights</Typography>
          <ReactTable
            title="Current Statistics"
            columns={columns}
            data={teamEvents}
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
