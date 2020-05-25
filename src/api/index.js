import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

/*TEAMS API CALLS*/

export const fetchTeams = async (active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/active/by/elo`);
    }
    else {
      teams = await axios.get(`${url}/teams/by/elo`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byRegion = async (region, active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/region/${region}/active/by/elo`);
    }
    else {
      teams = await axios.get(`${url}/teams/region/${region}/by/elo`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeams_byDistrict = async (district, active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/district/${district}/active/by/elo`);
    }
    else {
      teams = await axios.get(`${url}/teams/district/${district}/by/elo`);
    }
    return teams.data;
  } catch (error) {
    return error;
  }
}

/*TEAMS-YEAR API CALLS*/

export const fetchTeamYears = async (year) => {
  try {
    const teams = await axios.get(`${url}/teams/year/${year}/by/elo_max`);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeamYears_byRegion = async (region, year) => {
  try {
    const teams = await axios.get(`${url}/teams/region/${region}/year/${year}/by/elo_max`);
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeamYears_byDistrict = async (district, year) => {
  try {
    const teams = await axios.get(`${url}/teams/district/${district}/year/${year}/by/elo_max`);
    return teams.data;
  } catch (error) {
    return error;
  }
}

/*INDIVIDUAL TEAM API CALLS*/
export const fetchTeam = async (num) => {
  try {
    const team = await axios.get(`${url}/team/${num}/years`);
    console.log(team.data)
    return team.data
  } catch (error) {
    return error;
  }
}
