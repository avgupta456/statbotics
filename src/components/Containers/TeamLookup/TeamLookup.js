import React, { useState, useEffect } from "react";

import Paper from '@material-ui/core/Paper';

import { DropdownButton, Dropdown, Button } from "react-bootstrap";

import faker from 'faker';
import _ from 'lodash';

import { ReactTable } from './../../../components';
import { fetchTeams, fetchTeams_byRegion, fetchTeams_byDistrict } from './../../../api';
import styles from './TeamLookup.module.css';

export default function TeamLookup() {
  const [region, setRegion] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [title, setTitle] = useState("Team Lookup")
  const [data, setData] = useState([]);

  //column name, searchable, visible, filterable
  const columns = [
    ["Number", true, true, false],
    ["Name", true, true, false],
    ["Active", false, false, true],
    ["Current ELO", false, true, false],
    ["Recent ELO", false, true, false],
    ["Mean ELO", false, true, false],
    ["Max ELO", false, true, false],
  ];

  function clean(teams) {
    return teams.map(function(x, i){ return [
      x["team"],
      <a href={`teams/${x["team"]}`}>{x["name"]}</a>,
      (x["active"]?"Active":"Inactive"),
      x["elo"],
      x["elo_recent"],
      x["elo_mean"],
      x["elo_max"],
    ]});
  }

  useEffect(() => {
    const getTeams = async () => {
      const new_teams = await fetchTeams();
      setData(clean(new_teams.results));
    };

    const getTeams_byRegion = async () => {
      const new_teams = await fetchTeams_byRegion(region);
      setData(clean(new_teams.results));
    }

    const getTeams_byDistrict = async () => {
      const new_teams = await fetchTeams_byDistrict(district);
      setData(clean(new_teams.results));
    }

    if(format==="Teams") {getTeams()}
    else if(format==="Region") {getTeams_byRegion()}
    else {getTeams_byDistrict()}
  }, [format, region, district]);

  const addressDefinitions = faker.definitions.address
  const stateOptions = _.map(addressDefinitions.state, (state, index) => ({
    key: addressDefinitions.state_abbr[index],
    text: state,
  }));

  const countryOptions = [
    {key: "Australia", text: "Australia"},
    {key: "Brazil", text: "Brazil"},
    {key: "Canada", text: "Canada"},
    {key: "Chile", text: "Chile"},
    {key: "China", text: "China"},
    {key: "Israel", text: "Israel"},
    {key: "Mexico", text: "Mexico"},
    {key: "Netherlands", text: "Netherlands"},
    {key: "Turkey", text: "Turkey"},
  ]

  const districtOptions = [
    {key: "chs", text: "Chesapeake"},
    {key: "fim", text: "Michigan"},
    {key: "fin", text: "Indiana"},
    {key: "fit", text: "Texas"},
    {key: "fma", text: "Mid-Atlantic"},
    {key: "fnc", text: "North Carolina"},
    {key: "isr", text: "Israel"},
    {key: "ne", text: "New England"},
    {key: "ont", text: "Ontario"},
    {key: "pch", text: "Peachtree"},
    {key: "pnw", text: "Pacific NW"},
  ]

  function allClick() {
    setFormat("Teams")
    setTitle("Team Lookup");
  };

  function regionClick(key, value) {
    setRegion(key);
    setFormat("Region");
    setTitle(`Team Lookup - ${value}`);
  };

  function districtClick(key, value) {
    setDistrict(key);
    setFormat("District");
    setTitle(`Team Lookup - ${value}`);
  };


  return (
    <div>
      <Paper
        elevation={0}
        className = {styles.body}

        children = {
          <dir>

            <Button
              variant="primary"
              onClick={() => allClick()}
            >
              All Teams
            </Button>

            <DropdownButton title="Select US State">
              {stateOptions.map(x => (
                <Dropdown.Item
                  onClick={() => regionClick(x["key"], x["text"])}
                  key={x["key"]}
                >
                  {x["text"]}
                </Dropdown.Item>
              ))}
            </DropdownButton>

            <DropdownButton title="Select Country">
              {countryOptions.map( x => (
                <Dropdown.Item
                  onClick={()=>regionClick(x["key"], x["text"])}
                  key={x["key"]}
                >
                  {x["text"]}
                </Dropdown.Item>
              ))}
            </DropdownButton>

            <DropdownButton title="Select District">
              {districtOptions.map( x => (
                <Dropdown.Item
                  onClick={() => districtClick(x["key"])}
                  key={x["key"]}
                >
                  {x["text"]}
                </Dropdown.Item>
              ))}
            </DropdownButton>


            <ReactTable
              title={title}
              columns={columns}
              data={data}
            />
          </dir>
        }
      />
    </div>
  );
}
