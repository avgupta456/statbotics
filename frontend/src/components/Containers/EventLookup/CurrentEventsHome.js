import React, { useState, useEffect } from "react";

import { Paper, Typography } from "@material-ui/core";
import { Button } from "react-bootstrap";
import Select from "react-select";

import {
  fetchEvents,
  fetchEvents_byWeek,
  fetchEvents_byCountry,
  fetchEvents_byCountryWeek,
  fetchEvents_byState,
  fetchEvents_byStateWeek,
  fetchEvents_byDistrict,
  fetchEvents_byDistrictWeek,
} from "./../../../api";

import {
  countryOptions,
  usaOptions,
  canadaOptions,
  districtOptions,
  weekOptions,
} from "./../../../constants";

import styles from "./EventLookup.module.css";

export default function CurrentEventsHome() {
  const year = 2022;

  const [week, setWeek] = useState("None");

  const [country, setCountry] = useState("None");
  const [stateProv, setStateProv] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Events");

  const [weekDropdown, setWeekDropdown] = useState("Select Week");
  const [stateDropdown, setStateDropdown] = useState("Select State");
  const [countryDropdown, setCountryDropdown] = useState("Select Country");
  const [districtDropdown, setDistrictDropdown] = useState("Select District");

  const [ongoingEvents, setOngoingEvents] = useState([]);
  const [completedEvents, setCompletedEvents] = useState([]);
  const [upcomingEvents, setUpcomingEvents] = useState([]);

  useEffect(() => {
    const setEvents = (events) => {
      setOngoingEvents(events.filter((event) => event.status === "Ongoing"));
      setCompletedEvents(
        events.filter((event) => event.status === "Completed")
      );
      setUpcomingEvents(events.filter((event) => event.status === "Upcoming"));
    };

    const getEvents = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents(year);
      } else {
        new_events = await fetchEvents_byWeek(year, week);
      }
      setEvents(new_events);
    };

    const getEvents_byCountry = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents_byCountry(year, country);
      } else {
        new_events = await fetchEvents_byCountryWeek(year, country, week);
      }
      setEvents(new_events);
    };

    const getEvents_byState = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents_byState(year, country, stateProv);
      } else {
        new_events = await fetchEvents_byStateWeek(
          year,
          country,
          stateProv,
          week
        );
      }
      setEvents(new_events);
    };

    const getEvents_byDistrict = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents_byDistrict(year, district);
      } else {
        new_events = await fetchEvents_byDistrictWeek(year, district, week);
      }
      setEvents(new_events);
    };

    setEvents([]);
    if (format === "Events") {
      getEvents();
    } else if (format === "Country") {
      getEvents_byCountry();
    } else if (format === "State") {
      getEvents_byState();
    } else {
      getEvents_byDistrict();
    }
  }, [format, country, stateProv, district, year, week]);

  const weekClick = (week) => {
    setWeek(week["value"]);
    setWeekDropdown(week["label"]);
  };

  function allClick() {
    setFormat("Events");

    setWeek("None");
    setWeekDropdown("Select Week");

    setCountry("None");
    setCountryDropdown("Select Country");

    setStateProv("None");
    setStateDropdown("Select State");

    setDistrict("None");
    setDistrictDropdown("Select District");
  }

  const stateClick = (state) => {
    if (state["value"] === "All") {
      setFormat("Country");
    } else {
      setFormat("State");
    }

    if (usaOptions.includes(state)) {
      setCountry("USA");
      setCountryDropdown("USA");
    }

    setStateProv(state["value"]);
    setStateDropdown(state["label"]);

    setDistrict("None");
    setDistrictDropdown("Select District");
  };

  const countryClick = (country) => {
    setFormat("Country");
    setCountry(country["value"]);
    setCountryDropdown(country["label"]);

    setStateProv("None");
    if (country["label"] === "USA") {
      setStateDropdown("Select State");
    } else if (country["label"] === "Canada") {
      setStateDropdown("Select Province");
    } else {
      setStateDropdown("All");
    }

    setDistrict("None");
    setDistrictDropdown("Select District");
  };

  const districtClick = (district) => {
    setFormat("District");

    setCountry("None");
    setStateProv("None");
    setDistrict(district["value"]);

    setCountryDropdown("Select Country");
    setStateDropdown("Select State");
    setDistrictDropdown(district["label"]);
  };

  function getTopBar() {
    return (
      <div className={styles.button_group}>
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={weekOptions}
          onChange={weekClick}
          value={{ value: `${weekDropdown}`, label: `${weekDropdown}` }}
        />
        <Button
          variant="outline-dark"
          onClick={() => allClick()}
          className={styles.dropdown}
          children={<Typography>All Events</Typography>}
        />
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={countryOptions}
          onChange={countryClick}
          value={{
            value: `${countryDropdown}`,
            label: `${countryDropdown}`,
          }}
        />
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={
            country === "USA"
              ? usaOptions
              : country === "Canada"
              ? canadaOptions
              : usaOptions
          }
          onChange={stateClick}
          value={{ value: `${stateDropdown}`, label: `${stateDropdown}` }}
        />
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={districtOptions}
          onChange={districtClick}
          value={{
            value: `${districtDropdown}`,
            label: `${districtDropdown}`,
          }}
        />
      </div>
    );
  }

  return (
    <div>
      <Paper elevation={3} className={styles.body}>
        <div>
          {getTopBar()}
          <div>
            <p className={styles.header}>
              Ongoing Events ({ongoingEvents.length})
            </p>
            {ongoingEvents.slice(0, 5).map((event) => (
              <p>{event["name"]}</p>
            ))}
          </div>
          <div>
            <p className={styles.header}>
              Upcoming Events ({upcomingEvents.length})
            </p>
            {upcomingEvents.slice(0, 5).map((event) => (
              <p>{event["name"]}</p>
            ))}
          </div>
          <div>
            <p className={styles.header}>
              Completed Events ({completedEvents.length})
            </p>
            {completedEvents.slice(0, 5).map((event) => (
              <p>{event["name"]}</p>
            ))}
          </div>
        </div>
      </Paper>
    </div>
  );
}
