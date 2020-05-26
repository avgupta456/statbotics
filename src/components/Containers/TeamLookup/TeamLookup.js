import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import { Paper, Typography } from '@material-ui/core';
import { ButtonGroup, Button } from "react-bootstrap";
import Select from 'react-select';

import faker from 'faker';
import _ from 'lodash';

import { ReactTable } from './../../../components';
import { fetchTeams, fetchTeams_byRegion, fetchTeams_byDistrict } from './../../../api';
import styles from './TeamLookup.module.css';

export default function TeamLookup() {
  const [active, setActive] = useState(true)

  const [region, setRegion] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [title, setTitle] = useState("Team Lookup")
  const [data, setData] = useState([]);

  const [stateDropdown, setStateDropdown] = useState("Select State")
  const [countryDropdown, setCountryDropdown] = useState("Select Country")
  const [districtDropdown, setDistrictDropdown] = useState("Select District")

  //column name, searchable, visible, filterable
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, false, "Click names for details"],
    ["Rank", false, true, false, "By Current ELO"],
    ["Current ELO", false, true, false, "All ELOs are sortable"],
    ["Recent ELO", false, true, false, ""],
    ["Mean ELO", false, true, false, ""],
    ["Max ELO", false, true, false, ""],
  ];

  function clean(teams) {
    return teams.map(function(x, i){ return [
      x["team"],
      <Link to={`teams/${x["team"]}`} target="_blank">{x["name"]}</Link>,
      i+1,
      x["elo"],
      x["elo_recent"],
      x["elo_mean"],
      x["elo_max"],
    ]});
  }

  useEffect(() => {
    const getTeams = async () => {
      const new_teams = await fetchTeams(active, "elo");
      setData(clean(new_teams.results));
    };

    const getTeams_byRegion = async () => {
      const new_teams = await fetchTeams_byRegion(region, active, "elo");
      setData(clean(new_teams.results));
    }

    const getTeams_byDistrict = async () => {
      const new_teams = await fetchTeams_byDistrict(district, active, "elo");
      setData(clean(new_teams.results));
    }

    if(format==="Teams") {getTeams()}
    else if(format==="Region") {getTeams_byRegion()}
    else {getTeams_byDistrict()}
  }, [format, region, district, active]);

  const addressDefinitions = faker.definitions.address
  const stateOptions = _.map(addressDefinitions.state, (state, index) => ({
    value: addressDefinitions.state_abbr[index],
    label: state,
  }));

  const countryOptions = [
    {value: "Australia", label: "Australia"},
    {value: "Brazil", label: "Brazil"},
    {value: "Canada", label: "Canada"},
    {value: "China", label: "China"},
    {value: "Israel", label: "Israel"},
    {value: "Mexico", label: "Mexico"},
    {value: "Netherlands", label: "Netherlands"},
    {value: "Turkey", label: "Turkey"},
  ]

  const districtOptions = [
    {value: "chs", label: "Chesapeake"},
    {value: "fim", label: "Michigan"},
    {value: "fin", label: "Indiana"},
    {value: "fit", label: "Texas"},
    {value: "fma", label: "Mid-Atlantic"},
    {value: "fnc", label: "North Carolina"},
    {value: "isr", label: "Israel"},
    {value: "ne", label: "New England"},
    {value: "ont", label: "Ontario"},
    {value: "pch", label: "Peachtree"},
    {value: "pnw", label: "Pacific NW"},
  ]

  function activeClick() {
    setActive(!active)
  }

  function allClick() {
    setFormat("Teams")
    setTitle("Team Lookup");
    setStateDropdown("Select State")
    setCountryDropdown("Select Country")
    setDistrictDropdown("Select District")
  };

  const stateClick = (state) => {
    setRegion(state["value"]);
    setFormat("Region");
    setTitle(`Team Lookup - ${state["label"]}`);
    setStateDropdown(state["label"])
    setCountryDropdown("Select Country")
    setDistrictDropdown("Select District")
  }

  const countryClick = (country) => {
    setRegion(country["value"]);
    setFormat("Region");
    setTitle(`Team Lookup - ${country["label"]}`);
    setStateDropdown("Select State")
    setCountryDropdown(country["label"])
    setDistrictDropdown("Select District")
  }

  const districtClick = (district) => {
    setDistrict(district["value"]);
    setFormat("District");
    setTitle(`Team Lookup - ${district["label"]}`);
    setStateDropdown("Select State")
    setCountryDropdown("Select Country")
    setDistrictDropdown(district["label"])
  }

  return (
    <div>
      <Paper
        elevation={3}
        className = {styles.body}

        children = {
          <div>
          <ButtonGroup className={styles.button_group}>

          <Button
            variant="outline-dark"
            onClick={() => activeClick()}
            className={styles.button}
          >
              <Typography>{ active? "Include" : "Remove" } Inactives</Typography>
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
                menu: provided => ({ ...provided, zIndex: 9999 })
              }}
              options = {stateOptions}
              onChange = {stateClick}
              value = {{value:`${stateDropdown}`, label:`${stateDropdown}`}}
            />

            <Select
              className={styles.dropdown}
              styles={{
                menu: provided => ({ ...provided, zIndex: 9999 })
              }}
              options = {countryOptions}
              onChange = {countryClick}
              value = {{value:`${countryDropdown}`, label:`${countryDropdown}`}}
            />

            <Select
              className={styles.dropdown}
              styles={{
                menu: provided => ({ ...provided, zIndex: 9999 })
              }}
              options = {districtOptions}
              onChange = {districtClick}
              value = {{value:`${districtDropdown}`, label:`${districtDropdown}`}}
            />

            </ButtonGroup>

            <ReactTable
              title={title}
              columns={columns}
              data={data}
            />
          </div>
        }
      />
    </div>
  );
}
