import { Paper } from "@material-ui/core";
import React from "react";

import { usaOptions, canadaOptions } from "../../constants";

import styles from "./EventView.module.css";

export default function EventView({ event }) {
  const country = event.country;
  let state = "";
  if (country === "USA") {
    state = usaOptions.find((state) => state.value === event.state)?.label;
  } else if (country === "Canada") {
    state = canadaOptions.find((state) => state.value === event.state)?.label;
  }

  let district = "";
  if (event.district) {
    // convert event.district to uppercase and save as district
    district = event.district.toUpperCase();
  }

  let loc = country;
  if (state) {
    loc = `${state}, ${loc}`;
  }
  if (district) {
    loc = `${loc} (${district})`;
  }

  let status = "";
  if (event.current_match < 0) {
    status = "Upcoming";
  } else if (event.current_match === 0) {
    status = "Schedule Released";
  } else if (event.status === "Completed") {
    status = "Completed";
  } else if (event.current_match < event.qual_matches) {
    status = `Qual Match ${event.current_match}`;
  } else if (event.current_match === event.qual_matches) {
    status = "Quals Over";
  } else {
    status = "Elims Ongoing";
  }

  return (
    <Paper
      elevation={1}
      className={styles.container}
      style={{ backgroundColor: "#f8f8f8" }}
      onClick={() => {
        window.location.href = `/event/${event.key}`;
      }}
    >
      <strong>{event["name"]}</strong>
      <p>{loc}</p>
      <p>{status}</p>
      <p>{event.week}</p>
    </Paper>
  );
}
