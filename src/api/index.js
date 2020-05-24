import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

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
