import axios from "axios";

import { url } from "./index";

/*TEAMS API CALLS*/

export const fetchTeams_Simple = async () => {
  const key = "Teams_Simple";
  if (
    localStorage.getItem(key) !== undefined &&
    localStorage.getItem(key) !== null
  ) {
    const data = JSON.parse(localStorage.getItem(key));
    if (data.length > 6000) {
      return data;
    }
  }

  try {
    var teams = await axios.get(`${url}/teams`);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams = async (active, method) => {
  try {
    var teams;
    if (active) {
      teams = await axios.get(`${url}/teams/active/by/${method}`);
    } else {
      teams = await axios.get(`${url}/teams/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byCountry = async (country, active, method) => {
  try {
    var teams;
    if (active) {
      teams = await axios.get(
        `${url}/teams/country/${country}/active/by/${method}`
      );
    } else {
      teams = await axios.get(`${url}/teams/country/${country}/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byState = async (country, state, active, method) => {
  if (state === "All") {
    return fetchTeams_byCountry(country, active, method);
  }

  try {
    var teams;
    if (active) {
      teams = await axios.get(
        `${url}/teams/country/${country}/state/${state}/active/by/${method}`
      );
    } else {
      teams = await axios.get(
        `${url}/teams/country/${country}/state/${state}/by/${method}`
      );
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byDistrict = async (district, active, method) => {
  try {
    var teams;
    if (active) {
      teams = await axios.get(
        `${url}/teams/district/${district}/active/by/${method}`
      );
    } else {
      teams = await axios.get(`${url}/teams/district/${district}/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

/*INDIVIDUAL TEAM API CALLS*/

export const fetchTeam = async (num) => {
  try {
    const team = await axios.get(`${url}/team_years/team/${num}`);
    return team.data;
  } catch (error) {
    return error;
  }
};
