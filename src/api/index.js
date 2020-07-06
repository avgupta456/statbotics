import axios from "axios";

//const url = "https://backend.statbotics.io/api";
const url = 'http://localhost:8000/api';

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

/*TEAMS-YEAR API CALLS*/

export const fetchTeamsYear = async (year, method) => {
  try {
    const teams = await axios.get(`${url}/teams/year/${year}/by/${method}`);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byCountry = async (country, year, method) => {
  try {
    const teams = await axios.get(
      `${url}/teams/country/${country}/year/${year}/by/${method}`
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
      `${url}/teams/country/${country}/state/${state}/year/${year}/by/${method}`
    );
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byDistrict = async (district, year, method) => {
  try {
    const teams = await axios.get(
      `${url}/teams/district/${district}/year/${year}/by/${method}`
    );
    return teams.data;
  } catch (error) {
    return error;
  }
};

/*INDIVIDUAL TEAM API CALLS*/
export const fetchTeam = async (num) => {
  try {
    const team = await axios.get(`${url}/team/${num}/years`);
    return team.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamYearElo = async (num, year) => {
  try {
    if (num === 0) {
      return 0;
    }
    const team = await axios.get(`${url}/team/${num}/year/${year}`);
    return team.data[0].elo_max;
  } catch (error) {
    return 0;
  }
};
