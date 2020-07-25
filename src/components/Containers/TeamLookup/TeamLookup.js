import React, { useState, useEffect } from "react";

import { Paper, Typography } from "@material-ui/core";
import { Button } from "react-bootstrap";
import Select from "react-select";

import { ReactTable } from "./../../../components";

import {
  fetchTeams,
  fetchTeams_byCountry,
  fetchTeams_byState,
  fetchTeams_byDistrict,
} from "./../../../api";

import {
  countryOptions,
  usaOptions,
  canadaOptions,
  districtOptions,
} from "./../../../constants"

import styles from "./TeamLookup.module.css";

export default function TeamLookup() {
  const [active, setActive] = useState(true);

  const [country, setCountry] = useState("None");
  const [stateProv, setStateProv] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [title, setTitle] = useState("Team Lookup");
  const [data, setData] = useState([]);

  const [stateDropdown, setStateDropdown] = useState("Select State");
  const [countryDropdown, setCountryDropdown] = useState("Select Country");
  const [districtDropdown, setDistrictDropdown] = useState("Select District");

  //column name, searchable, visible, link, hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click names for details"],
    ["Rank", false, true, false, "By Current Elo"],
    ["Current Elo", false, true, false, "All Elos are sortable"],
    ["Recent Elo", false, true, false, ""],
    ["Mean Elo", false, true, false, ""],
    ["Max Elo", false, true, false, ""],
  ];

  //Link format is assumed "team number|team name"
  function clean(teams) {
    return teams.map(function (x, i) {
      return [
        x["team"],
        x["team"] + "|" + x["name"],
        i + 1,
        x["elo"],
        x["elo_recent"],
        x["elo_mean"],
        x["elo_max"],
      ];
    });
  }

  useEffect(() => {
    const getTeams = async () => {
      const new_teams = await fetchTeams(active, "-elo");
      setData(clean(new_teams));
    };

    const getTeams_byCountry = async () => {
      const new_teams = await fetchTeams_byCountry(country, active, "-elo");
      setData(clean(new_teams));
    };

    const getTeams_byState = async () => {
      const new_teams = await fetchTeams_byState(
        country,
        stateProv,
        active,
        "-elo"
      );
      setData(clean(new_teams));
    };

    const getTeams_byDistrict = async () => {
      const new_teams = await fetchTeams_byDistrict(district, active, "-elo");
      setData(clean(new_teams));
    };

    if (format === "Teams") {
      getTeams();
    } else if (format === "Country") {
      getTeams_byCountry();
    } else if (format === "State") {
      getTeams_byState();
    } else {
      getTeams_byDistrict();
    }
  }, [format, country, stateProv, district, active]);

  function activeClick() {
    setActive(!active);
  }

  function allClick() {
    setFormat("Teams");
    setTitle("Team Lookup");

    setCountryDropdown("Select Country");
    setStateDropdown("Select State");
    setDistrictDropdown("Select District");
  }

  const stateClick = (state) => {
    setFormat("State");
    if (state["value"] === "All") {
      setTitle(`Team Lookup - ${country}`);
    } else {
      setTitle(`Team Lookup - ${state["label"]}`);
    }

    if (usaOptions.includes(state)) {
      setCountry("USA");
    }
    setStateProv(state["value"]);

    if (usaOptions.includes(state)) {
      setCountryDropdown("USA");
    }
    setStateDropdown(state["label"]);
    setDistrictDropdown("Select District");
  };

  const countryClick = (country) => {
    setFormat("Country");
    setTitle(`Team Lookup - ${country["label"]}`);

    setCountry(country["value"]);

    setCountryDropdown(country["label"]);
    if (country["label"] === "USA") {
      setStateDropdown("Select State");
    } else if (country["label"] === "Canada") {
      setStateDropdown("Select Province");
    } else {
      setStateDropdown("All");
    }
    setDistrictDropdown("Select District");
  };

  const districtClick = (district) => {
    setFormat("District");
    setTitle(`Team Lookup - ${district["label"]}`);

    setCountry("None");
    setStateProv("None");
    setDistrict(district["value"]);

    setStateDropdown("Select State");
    setCountryDropdown("Select Country");
    setDistrictDropdown(district["label"]);
  };

  return (
    <div>
      <Paper elevation={3} className={styles.body}>
        <div>
          <div className={styles.button_group}>
            <Button
              variant="outline-dark"
              onClick={() => activeClick()}
              className={styles.dropdown}
            >
              <Typography>{active ? "Include" : "Remove"} Inactives</Typography>
            </Button>
            <Button
              variant="outline-dark"
              onClick={() => allClick()}
              className={styles.dropdown}
            >
              <Typography>All Teams</Typography>
            </Button>
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
          <ReactTable title={title} columns={columns} data={data} />
        </div>
      </Paper>
    </div>
  );
}
