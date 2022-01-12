import axios from "axios";

import { url } from "./index";

/*TEAMS-YEAR API CALLS*/

export const fetchTeamsYear = async (year, method) => {
  try {
    let completeUrl = `${url}/team_years/year/${year}`;
    if (method) {
      completeUrl += `/by/${method}`;
    }
    const teams = await axios.get(completeUrl);
    return teams.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

export const fetchTeamsYear_byCountry = async (country, year, method) => {
  try {
    let completeUrl = `${url}/team_years/year/${year}/country/${country}`;
    if (method) {
      completeUrl += `/by/${method}`;
    }
    const teams = await axios.get(completeUrl);
    return teams.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

export const fetchTeamsYear_byState = async (country, state, year, method) => {
  if (state === "All") {
    return fetchTeamsYear_byCountry(country, year, method);
  }

  try {
    let completeUrl = `${url}/team_years/year/${year}/country/${country}/state/${state}`;
    if (method) {
      completeUrl += `/by/${method}`;
    }
    const teams = await axios.get(completeUrl);
    return teams.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

export const fetchTeamsYear_byDistrict = async (district, year, method) => {
  try {
    let completeUrl = `${url}/team_years/year/${year}/district/${district}`;
    if (method) {
      completeUrl += `/by/${method}`;
    }
    const teams = await axios.get(completeUrl);
    return teams.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

/*INDIVIDUAL TEAM API CALLS*/

export const fetchTeam_Years = async (num) => {
  try {
    const team = await axios.get(`${url}/team_years/team/${num}`);
    return team.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

/*INDIVIDUAL TEAM YEAR*/

export const fetchTeamYearElo = async (num, year) => {
  try {
    if (num === 0) {
      return 0;
    }
    const team = await axios.get(`${url}/team_year/team/${num}/year/${year}`);
    return team.data[0].elo_max;
  } catch (error) {
    console.log(error);
    return 0;
  }
};
