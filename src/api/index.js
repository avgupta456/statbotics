import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

/*TEAMS API CALLS*/

export const fetchTeams = async (active, method) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/active/by/${method}`);
    }
    else {
      teams = await axios.get(`${url}/teams/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byRegion = async (region, active, method) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/region/${region}/active/by/${method}`);
    }
    else {
      teams = await axios.get(`${url}/teams/region/${region}/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeams_byDistrict = async (district, active, method) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/district/${district}/active/by/${method}`);
    }
    else {
      teams = await axios.get(`${url}/teams/district/${district}/by/${method}`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
}

/*TEAMS-YEAR API CALLS*/

export const fetchTeamsYear = async (year, method) => {
  try {
    const teams = await axios.get(`${url}/teams/year/${year}/by/${method}`);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamsYear_byRegion = async (region, year, method) => {
  try {
    const teams = await axios.get(`${url}/teams/region/${region}/year/${year}/by/${method}`);
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeamsYear_byDistrict = async (district, year, method) => {
  try {
    const teams = await axios.get(`${url}/teams/district/${district}/year/${year}/by/${method}`);
    return teams.data;
  } catch (error) {
    return error;
  }
}

/*INDIVIDUAL TEAM API CALLS*/
export const fetchTeam = async (num) => {
  try {
    const team = await axios.get(`${url}/team/${num}/years`);
    return team.data
  } catch (error) {
    return error;
  }
}

export const fetchTeamYear = async (num, year) => {
  try {
    const team = await axios.get(`${url}/team/${num}/year/${year}`);
    return team.data
  } catch (error) {
    return error;
  }
}
