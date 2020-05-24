import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

export const fetchTeams = async (active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/active/by/elo_recent`);
    }
    else {
      teams = await axios.get(`${url}/teams/by/elo_recent`);
    }
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byRegion = async (region, active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/region/${region}/by/elo_recent`);
    }
    else {
      teams = await axios.get(`{url}/teams/region/${region}/active/by/elo_recent`);
    }
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeams_byDistrict = async (district, active) => {
  try {
    var teams;
    if(active) {
      teams = await axios.get(`${url}/teams/district/${district}/active/by/elo_recent`);
    }
    else {
      teams = await axios.get(`${url}/teams/district/${district}/by/elo_recent`);
    }
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
}
