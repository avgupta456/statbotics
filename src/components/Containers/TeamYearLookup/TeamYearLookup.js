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
  yearOptions,
} from "./../../../constants"

import styles from "./TeamYearLookup.module.css";

export default function TeamLookup() {
  const [year, setYear] = useState(2020);

  const [country, setCountry] = useState("None");
  const [stateProv, setStateProv] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [title, setTitle] = useState(`${year} Team Lookup`);
  const [data, setData] = useState([]);

  const [stateDropdown, setStateDropdown] = useState("Select State");
  const [countryDropdown, setCountryDropdown] = useState("Select Country");
  const [districtDropdown, setDistrictDropdown] = useState("Select District");

  //column name, searchable, visible, link, hint
  const eloColumns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click names for details"],
    ["Rank", false, true, false, "By Max Elo"],
    ["Max Elo", false, true, false, "All Elos are sortable"],
    ["Mean Elo", false, true, false, ""],
    ["Start Elo", false, true, false, ""],
    ["Pre Champs Elo", false, false, false, ""],
    ["End Elo", false, true, false, ""],
  ];

  const OPRColumns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click names for details"],
    ["Rank", false, true, false, "By OPR"],
    ["OPR", false, true, false, "Max OPR"],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    ["ILS 1", false, true, false, ""],
    ["ILS 2", false, true, false, ""],
  ]

  const [showElo, setShowElo] = useState(true)
  const [sortBy, setSortBy] = useState("-elo_max")

  const handleElo = (event) => {
    // backwards since we invert afterwards
    if (!showElo) setSortBy("-elo_max")
    else if (year>=2016) setSortBy("-opr_no_fouls")
    else setSortBy("-opr")
    setShowElo(!showElo)
  }

  useEffect(() => {
    function clean(teams) {
      if(showElo) {
        return teams.map(function (x, i) {
          return [
            x["team"],
            "teams/" + x["team"] + "|" + x["name"],
            i + 1,
            x["elo_max"],
            x["elo_mean"],
            x["elo_start"],
            x["elo_pre_champs"],
            x["elo_end"],
          ];
        });
      }
      else if (year>=2016) {
        return teams.map(function (x, i) {
          return [
            x["team"],
            "teams/" + x["team"] + "|" + x["name"],
            i + 1,
            parseInt(x["opr_no_fouls"]*10)/10,
            parseInt(x["opr_auto"]*10)/10,
            parseInt(x["opr_teleop"]*10)/10,
            parseInt(x["opr_endgame"]*10)/10,
            x["ils_1"],
            x["ils_2"],
          ];
        });
      }
      else {
        return teams.map(function (x, i) {
          return [
            x["team"],
            "teams/" + x["team"] + "|" + x["name"],
            i + 1,
            parseInt(x["opr"]*10)/10,
            -1,
            -1,
            -1,
            -1,
            -1,
          ];
        });
      }
    }

    const getTeams = async () => {
      const new_teams = await fetchTeamsYear(year, sortBy);
      setData(clean(new_teams));
    };

    const getTeams_byCountry = async () => {
      const new_teams = await fetchTeamsYear_byCountry(
        country,
        year,
        sortBy
      );
      setData(clean(new_teams));
    };

    const getTeams_byState = async () => {
      const new_teams = await fetchTeamsYear_byState(
        country,
        stateProv,
        year,
        sortBy
      );
      setData(clean(new_teams));
    };

    const getTeams_byDistrict = async () => {
      const new_teams = await fetchTeamsYear_byDistrict(
        district,
        year,
        sortBy
      );
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
  }, [format, country, stateProv, district, year, showElo, sortBy]);

  const yearClick = (year) => {
    setYear(year["value"]);
    setTitle(`${year["value"]} Team Lookup`);
  };

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
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={yearOptions}
          onChange={yearClick}
          value={{ value: `${year}`, label: `${year}` }}
        />
        <Button
          variant="outline-dark"
          onClick={() => allClick()}
          className={styles.dropdown}
          children={<Typography>All Teams</Typography>}
        />
        <Button
          variant="secondary"
          onClick={() => handleElo()}
          className={styles.dropdown}
          children={<Typography>{showElo ? "Show OPR" : "Show Elo"}</Typography>}
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
    )
  }

  return (
    <div>
      <Paper
        elevation={3}
        className={styles.body}
        children={
          <div>
            {getTopBar()}
            <ReactTable title={title} columns={showElo ? eloColumns: OPRColumns} data={data} />
          </div>
        }
      />
    </div>
  );
}
