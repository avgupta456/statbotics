import React, { useEffect } from "react";

import WindowedSelect from "react-windowed-select";
import { fetchTeams_Simple, fetchEvents_Simple } from "./../../api";

export default function TeamSelect({ className, onChange, isMulti }) {
  const [teams, setTeams] = React.useState([]);
  const [events, setEvents] = React.useState([]);
  const max_length = 30;

  function cleanTeams(teams) {
    return teams.map(function (x, i) {
      if (x["name"].length > max_length) {
        x["name"] = x["name"].substring(0, max_length - 3) + "...";
      }
      return {
        value: "/teams/" + x["key"],
        label: x["team"] + " | " + x["name"],
      };
    });
  }

  function cleanEvents(events) {
    return events.map(function (x, i) {
      if (x["name"].length > max_length) {
        x["name"] = x["name"].substring(0, max_length - 3) + "...";
      }
      return {
        value: "/events/" + x["key"],
        label: x["year"] + " " + x["name"],
      };
    });
  }

  useEffect(() => {
    const getTeams = async () => {
      const newTeams = await fetchTeams_Simple();
      const key = "Search_Teams";
      localStorage.setItem(key, JSON.stringify(newTeams));
      setTeams(cleanTeams(newTeams));
    };

    const getEvents = async () => {
      const newEvents = await fetchEvents_Simple();
      const key = "Search_Events";
      localStorage.setItem(key, JSON.stringify(newEvents));
      setEvents(cleanEvents(newEvents));
    };

    if (teams.length === 0) {
      getTeams();
    }
    if (events.length === 0) {
      getEvents();
    }
    console.log(teams);
    console.log(events);
    console.log(teams.concat(events));
  }, [teams, events]);

  return (
    <WindowedSelect
      placeholder={"Search Teams and Events"}
      className={className}
      isMulti={isMulti}
      onChange={onChange}
      options={teams.concat(events)}
    />
  );
}
