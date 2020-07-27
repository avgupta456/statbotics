import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { Paper, Typography } from "@material-ui/core";
import { Tabs, Tab } from "react-bootstrap";

import { fetchEvent } from "./../../../api";

import styles from "./EventView.module.css";

export default function EventView() {
  let { key } = useParams();

  const [event, setEvent] = useState("");

  useEffect(() => {
    const getEvent = async (key) => {
      const event = await fetchEvent(key);
      console.log(event);
      setEvent(event["name"]);
    };
    console.log(key);
    getEvent(key);
  }, [key]);

  return (
    <Paper className={styles.body}>
      <h2>{event}</h2>
      <br />
      <Tabs defaultActiveKey="insights" id="tab">
        <Tab eventKey="insights" title="Insights">
          <Typography>Insights</Typography>
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
