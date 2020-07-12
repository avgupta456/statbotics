import React, { useState, useEffect } from "react";

import { Paper, Typography } from "@material-ui/core";
import { ButtonGroup, Button } from "react-bootstrap";
import Select from "react-select";

import faker from "faker";
import _ from "lodash";

import { ReactTable } from "./../../../components";

import {
  fetchTeams,
  fetchTeams_byCountry,
  fetchTeams_byState,
  fetchTeams_byDistrict,
} from "./../../../api";

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

  const countryOptions = [
    { value: "USA", label: "USA" },
    { value: "Canada", label: "Canada" },
    { value: "Turkey", label: "Turkey" },
    { value: "Israel", label: "Israel" },
    { value: "China", label: "China" },
    { value: "Mexico", label: "Mexico" },
    { value: "Australia", label: "Australia" },
    { value: "Brazil", label: "Brazil" },
    { value: "Chinese Taipei", label: "Chinese Taipei" },
    { value: "Netherlands", label: "Netherlands" },
    { value: "Chile", label: "Chile" },
    { value: "United Kingdom", label: "United Kingdom" },
    { value: "Colombia", label: "Colombia" },
    { value: "Japan", label: "Japan" },
    { value: "Poland", label: "Poland" },
    { value: "India", label: "India" },
    { value: "Switzerland", label: "Switzerland" },
  ];

  const addressDefinitions = faker.definitions.address;
  const usaOptions = _.map(addressDefinitions.state, (state, index) => ({
    value: addressDefinitions.state_abbr[index],
    label: state,
  }));

  usaOptions.unshift({ value: "All", label: "All" });

  const canadaOptions = [
    { value: "All", label: "All" },
    { value: "AB", label: "Alberta" },
    { value: "BC", label: "British Columbia" },
    { value: "MB", label: "Manitoba" },
    { value: "ON", label: "Ontario" },
    { value: "QC", label: "Québec" },
    { value: "SK", label: "Saskatchewan" },
  ];

  const districtOptions = [
    { value: "chs", label: "Chesapeake" },
    { value: "fim", label: "Michigan" },
    { value: "fin", label: "Indiana" },
    { value: "fit", label: "Texas" },
    { value: "fma", label: "Mid-Atlantic" },
    { value: "fnc", label: "North Carolina" },
    { value: "isr", label: "Israel" },
    { value: "ne", label: "New England" },
    { value: "ont", label: "Ontario" },
    { value: "pch", label: "Peachtree" },
    { value: "pnw", label: "Pacific NW" },
  ];

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
          <ButtonGroup className={styles.button_group}>
            <Button
              variant="outline-dark"
              onClick={() => activeClick()}
              className={styles.button}
            >
              <Typography>{active ? "Include" : "Remove"} Inactives</Typography>
            </Button>

            <Button
              variant="outline-dark"
              onClick={() => allClick()}
              className={styles.button}
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
          </ButtonGroup>
          <ReactTable title={title} columns={columns} data={data} />
        </div>
      </Paper>
    </div>
  );
}
