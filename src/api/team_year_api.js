import axios from "axios";

import { url } from "./index";

/*TEAMS-YEAR API CALLS*/

export const fetchTeamsYear = async (year, method) => {
  try {
    const teams = await axios.get(
      `${url}/team_years/year/${year}/by/${method}`
    );
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byCountry = async (country, year, method) => {
  try {
    const teams = await axios.get(
      `${url}/team_years/year/${year}/country/${country}/by/${method}`
    );
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byState = async (country, state, year, method) => {
  if (state === "All") {
    return fetchTeamsYear_byCountry(country, year, method);
  }

  try {
    const teams = await axios.get(
      `${url}/team_years/year/${year}/country/${country}/state/${state}/by/${method}`
    );
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byDistrict = async (district, year, method) => {
  try {
    const teams = await axios.get(
      `${url}/team_years/year/${year}/district/${district}/by/${method}`
    );
    return teams.data;
  } catch (error) {
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
    return 0;
  }
};
