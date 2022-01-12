import React, { useState, useEffect } from "react";

import { Paper, Typography } from "@material-ui/core";

import { Button } from "react-bootstrap";
import Select from "react-select";

import { ReactTable } from "./../../../components";

import {
  fetchTeamsYear,
  fetchTeamsYear_byCountry,
  fetchTeamsYear_byState,
  fetchTeamsYear_byDistrict,
} from "./../../../api";

import {
  countryOptions,
  usaOptions,
  canadaOptions,
  districtOptions,
} from "./../../../constants";

import styles from "./TeamYearLookup.module.css";

export default function TeamLookup() {
  const year = 2022;

  const [country, setCountry] = useState("None");
  const [stateProv, setStateProv] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [title, setTitle] = useState(`${year} Team Lookup`);
  const [data, setData] = useState([]);

  const [stateDropdown, setStateDropdown] = useState("Select State");
  const [countryDropdown, setCountryDropdown] = useState("Select Country");
  const [districtDropdown, setDistrictDropdown] = useState("Select District");

  // Name, Searchable, Visible, Link, Hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Elo", false, true, false, ""],
    ["OPR", false, true, false, ""],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    ["Winrate", false, true, false, ""],
  ];

  useEffect(() => {
    function clean(teams) {
      let newTeams = teams.map((x) => {
        const elo = x["elo_end"] > 0 ? x["elo_end"] : x["elo_start"];
        const opr = x["opr_no_fouls"] > 0 ? x["opr_no_fouls"] : x["opr"];
        return [
          x["team"],
          "team/" + x["team"] + "|" + x["name"],
          elo,
          parseInt(opr * 10) / 10,
          parseInt(x["opr_auto"] * 10) / 10,
          parseInt(x["opr_teleop"] * 10) / 10,
          parseInt(x["opr_endgame"] * 10) / 10,
          parseInt(x["winrate"] * 1000) / 10 + "%",
        ];
      });

      newTeams = newTeams.sort((a, b) => b[2] - a[2]);
      return newTeams;
    }

    const getTeams = async () => {
      const new_teams = await fetchTeamsYear(year);
      setData(clean(new_teams));
    };

    const getTeams_byCountry = async () => {
      const new_teams = await fetchTeamsYear_byCountry(country, year);
      setData(clean(new_teams));
    };

    const getTeams_byState = async () => {
      const new_teams = await fetchTeamsYear_byState(country, stateProv, year);
      setData(clean(new_teams));
    };

    const getTeams_byDistrict = async () => {
      const new_teams = await fetchTeamsYear_byDistrict(district, year);
      setData(clean(new_teams));
    };

    setData([]);
    if (format === "Teams") {
      getTeams();
    } else if (format === "Country") {
      getTeams_byCountry();
    } else if (format === "State") {
      getTeams_byState();
    } else {
      getTeams_byDistrict();
    }
  }, [format, country, stateProv, district, year]);

  function allClick() {
    setFormat("Teams");

    setCountry("None");
    setCountryDropdown("Select Country");

    setStateProv("None");
    setStateDropdown("Select State");

    setDistrict("None");
    setDistrictDropdown("Select District");

    setTitle(`${year} Team Lookup`);
  }

  const stateClick = (state) => {
    if (state["value"] === "All") {
      setTitle(`${year} Team Lookup - ${country}`);
      setFormat("Country");
    } else {
      setTitle(`${year} Team Lookup - ${state["label"]}`);
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
    setTitle(`${year} Team Lookup - ${country["label"]}`);

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
    setTitle(`${year} Team Lookup - ${district["label"]}`);

    setCountry("None");
    setCountryDropdown("Select Country");

    setStateProv("None");
    setStateDropdown("Select State");

    setDistrict(district["value"]);
    setDistrictDropdown(district["label"]);
  };

  function getTopBar() {
    return (
      <div className={styles.button_group}>
        <Button
          variant="outline-dark"
          onClick={() => allClick()}
          className={styles.dropdown}
          children={<Typography>All Teams</Typography>}
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
      <Paper
        elevation={3}
        className={styles.body}
        children={
          <div>
            {getTopBar()}
            <ReactTable title={title} columns={columns} data={data} />
          </div>
        }
      />
    </div>
  );
}
