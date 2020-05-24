import React, { useState, useEffect } from "react";

import Paper from '@material-ui/core/Paper';

import { DropdownButton, Dropdown } from "react-bootstrap";

import faker from 'faker';
import _ from 'lodash';

import { ReactTable } from './../../../components';
import { fetchTeams, fetchTeams_byRegion, fetchTeams_byDistrict } from './../../../api';
import styles from './TeamLookup.module.css';

export default function TeamLookup() {
  const [region, setRegion] = useState("None");
  const [district, setDistrict] = useState("None");
  const [format, setFormat] = useState("Teams");
  const [data, setData] = useState([]);

  //column name, searchable, visible, filterable
  const columns = [
    ["Number", true, true, false],
    ["Name", true, true, false],
    ["Active", false, false, true],
    ["District", false, false, false],
    ["Region", false, false, false],
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
      x["district"],
      x["region"],
      x["elo"],
      x["elo_recent"],
      x["elo_mean"],
      x["elo_max"],
    ]});
  }

  useEffect(() => {
    const getTeams = async () => {
      console.log("getTeams")
      const new_teams = await fetchTeams();
      console.log(clean(new_teams.results))
      setData(clean(new_teams.results));
      console.log(data)
    };

    const getTeams_byRegion = async () => {
      console.log("getTeams_byRegion")
      const new_teams = await fetchTeams_byRegion(region);
      console.log(new_teams.results)
      setData(clean(new_teams.results));
      console.log(data)
    }

    const getTeams_byDistrict = async () => {
      console.log("getTeams_byDistrict")
      const new_teams = await fetchTeams_byDistrict(district);
      console.log(new_teams.results)
      setData(clean(new_teams.results));
      console.log(data)
    }

    if(format==="Teams") {
      getTeams()
    }
    else if(format==="Region") {
      getTeams_byRegion()
    }
    else {
      getTeams_byDistrict()
    }
  }, [format, region, district]);


  const addressDefinitions = faker.definitions.address
  const stateOptions = _.map(addressDefinitions.state, (state, index) => ({
    key: addressDefinitions.state_abbr[index],
    text: state,
  }));

  function regionClick(key) {
    setRegion(key);
    setFormat("Region");
  };

  function districtClick(key) {
    setDistrict(key);
    setFormat("District");
  }

  return (
    <div>
      <Paper
        elevation={0}
        className = {styles.body}

        children = {
          <dir>
            <DropdownButton title="Select State">
              {stateOptions.map( x => (<Dropdown.Item onClick={() => regionClick(x["key"])} key={x["key"]}>{x["text"]}</Dropdown.Item>))}
            </DropdownButton>
            <DropdownButton title="Select District">
              {stateOptions.map( x => (<Dropdown.Item onClick={() => districtClick(x["key"])} key={x["key"]}>{x["text"]}</Dropdown.Item>))}
            </DropdownButton>
            <ReactTable title={"Team Lookup"} columns={columns} data={data}/>
            <h1>{region}</h1>
            <h1>{district}</h1>
            <h1>{format}</h1>
          </dir>
        }
      />
    </div>
  );
}
