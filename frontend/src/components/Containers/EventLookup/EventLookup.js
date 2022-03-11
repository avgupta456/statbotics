import React, { useState, useEffect } from "react";

import { Paper, Typography } from "@material-ui/core";
import { Button } from "react-bootstrap";
import Select from "react-select";

import { ReactTable } from "./../../../components";

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
  yearOptions,
  weekOptions,
} from "./../../../constants";

import styles from "./EventLookup.module.css";

export default function EventLookup() {
  const [year, setYear] = useState(2020);
  const [week, setWeek] = useState("None");

  const [country, setCountry] = useState("None");
  const [stateProv, setStateProv] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Events");
  const [title, setTitle] = useState("Events Lookup");
  const [data, setData] = useState([]);

  const [weekDropdown, setWeekDropdown] = useState("Select Week");
  const [stateDropdown, setStateDropdown] = useState("Select State");
  const [countryDropdown, setCountryDropdown] = useState("Select Country");
  const [districtDropdown, setDistrictDropdown] = useState("Select District");

  //column name, searchable, visible, link, hint
  const columns = [
    ["Key", true, true, false, ""],
    ["Name", true, true, true, ""],
    ["Week", false, true, false, "Competition Week"],
    ["Top 8 Elo", false, true, false, "Average of Top 8 Elos"],
    ["Top 24 Elo", false, true, false, "Average of Top 24 Elos"],
    ["Mean Elo", false, true, false, ""],
    ["Top 8 OPR", false, true, false, "Average of Top 8 OPRs"],
    ["Top 24 OPR", false, true, false, "Average of Top 24 OPRs"],
    ["Mean OPR", false, true, false, ""],
  ];

  useEffect(() => {
    function clean(events) {
      return events.map(function (x, i) {
        return [
          x["key"],
          "event/" + x["key"] + "|" + x["name"],
          x["week"],
          x["elo_top8"],
          x["elo_top24"],
          x["elo_mean"],
          parseInt(x["opr_top8"] * 10) / 10,
          parseInt(x["opr_top24"] * 10) / 10,
          parseInt(x["opr_mean"] * 10) / 10,
        ];
      });
    }

    const getEvents = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents(year);
      } else {
        new_events = await fetchEvents_byWeek(year, week);
      }
      setData(clean(new_events));
    };

    const getEvents_byCountry = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents_byCountry(year, country);
      } else {
        new_events = await fetchEvents_byCountryWeek(year, country, week);
      }
      setData(clean(new_events));
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
      setData(clean(new_events));
    };

    const getEvents_byDistrict = async () => {
      let new_events;
      if (week === "None") {
        new_events = await fetchEvents_byDistrict(year, district);
      } else {
        new_events = await fetchEvents_byDistrictWeek(year, district, week);
      }
      setData(clean(new_events));
    };

    setData([]);
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

  const yearClick = (year) => {
    setYear(year["value"]);

    setWeek("None");
    setWeekDropdown("Select Week");

    setTitle(`${year["value"]} Event Lookup`);
  };

  const weekClick = (week) => {
    setWeek(week["value"]);
    setWeekDropdown(week["label"]);

    setTitle(`${year} Event Lookup`);
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

    setTitle(`${year} Event Lookup`);
  }

  const stateClick = (state) => {
    if (state["value"] === "All") {
      setTitle(`${year} Event Lookup - ${country}`);
      setFormat("Country");
    } else {
      setTitle(`${year} Event Lookup - ${state["label"]}`);
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
    setTitle(`${year} Event Lookup - ${country["label"]}`);

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
    setTitle(`${year} Event Lookup - ${district["label"]}`);

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
          options={yearOptions}
          onChange={yearClick}
          value={{ value: `${year}`, label: `${year}` }}
        />
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
          <ReactTable title={title} columns={columns} data={data} />
        </div>
      </Paper>
    </div>
  );
}
