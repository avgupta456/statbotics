import React from "react";

import { Card, CardContent, Typography } from "@material-ui/core";

import styles from "./EventView.module.css";

export default function EventView({ event }) {
  const country = event.country;
  const state = event.state === "All" ? null : event.state;

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

  let status = null;
  if (event.status === "Upcoming" || event.status === "Completed") {
    status = null;
  } else if (event.current_match === 0) {
    status = "Schedule Released";
  } else if (event.current_match < event.qual_matches) {
    status = `Qual Match ${event.current_match}`;
  } else if (event.current_match === event.qual_matches) {
    status = "Quals Over";
  } else {
    status = "Elims Ongoing";
  }

  let name = event.name;
  if (name.length > 35) {
    name = name.substring(0, 32) + "...";
  }

  return (
    <Card
      className={styles.container}
      onClick={() => {
        window.location.href = `/event/${event.key}`;
      }}
    >
      <CardContent>
        <Typography variant="h6" component="div">
          <strong>{name}</strong>
        </Typography>
        <Typography color="text.secondary">
          {loc} - Week {event.week}
        </Typography>
        <Typography>{status}</Typography>
      </CardContent>
    </Card>
  );
}
