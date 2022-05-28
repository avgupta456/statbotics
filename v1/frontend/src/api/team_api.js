import axios from "axios";

import { url } from "./index";
import { getWithExpiry } from "./local_storage";

/*TEAMS API CALLS*/

export const fetchTeams_Simple = async () => {
  const key = "Search_Teams";
  const data = getWithExpiry(key);
  if (data && data.length > 6000) {
    return data;
  }

  try {
    var teams = await axios.get(`${url}/teams`);
    return teams.data;
  } catch (error) {
    console.log(error);
    return error;
  }
};

export const fetchTeams = async (active, method) => {
  try {
    let completeUrl = `${url}/teams`;
    if (active) {
      completeUrl += `/active`;
    }
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

export const fetchTeams_byCountry = async (country, active, method) => {
  try {
    let completeUrl = `${url}/teams/country/${country}`;
    if (active) {
      completeUrl += `/active`;
    }
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

export const fetchTeams_byState = async (country, state, active, method) => {
  if (state === "All") {
    return fetchTeams_byCountry(country, active, method);
  }

  try {
    let completeUrl = `${url}/teams/country/${country}/state/${state}`;
    if (active) {
      completeUrl += `/active`;
    }
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

export const fetchTeams_byDistrict = async (district, active, method) => {
  try {
    let completeUrl = `${url}/teams/district/${district}`;
    if (active) {
      completeUrl += `/active`;
    }
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

export const fetchTeam = async (number) => {
  try {
    const team = await axios.get(`${url}/team/${number}`);
    return team.data[0];
  } catch (error) {
    console.log(error);
    return error;
  }
};
