import React, { useEffect } from "react";

import WindowedSelect from "react-windowed-select";
import { setWithExpiry } from "../../api/local_storage";
import { fetchTeams_Simple, fetchEvents_Simple } from "./../../api";

export default function TeamSelect({
  className,
  onChange,
  isMulti,
  includeEvents,
}) {
  const [teams, setTeams] = React.useState([]);
  const [events, setEvents] = React.useState([]);
  const [text, setText] = React.useState("Search Teams");
  const max_length = 30;

  function cleanTeams(teams) {
    return teams.map(function (x, i) {
      if (x["name"].length > max_length) {
        x["name"] = x["name"].substring(0, max_length - 3) + "...";
      }
      return {
        value: "/team/" + x["team"],
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
        value: "/event/" + x["key"],
        label: x["year"] + " " + x["name"],
      };
    });
  }

  useEffect(() => {
    const getTeams = async () => {
      const newTeams = await fetchTeams_Simple();
      const key = "Search_Teams";
      setWithExpiry(key, newTeams, 60 * 60 * 24);
      setTeams(cleanTeams(newTeams));
    };

    const getEvents = async () => {
      const newEvents = await fetchEvents_Simple();
      const key = "Search_Events";
      setWithExpiry(key, newEvents, 60 * 60 * 24);
      setEvents(cleanEvents(newEvents));
    };

    if (teams.length === 0) {
      getTeams();
    }
    if (events.length === 0 && includeEvents) {
      getEvents();
    }

    if (includeEvents) {
      setText("Search Teams and Events");
    }
  }, [teams, events, includeEvents]);

  return (
    <WindowedSelect
      placeholder={text}
      className={className}
      isMulti={isMulti}
      onChange={onChange}
      options={teams.concat(events)}
    />
  );
}
