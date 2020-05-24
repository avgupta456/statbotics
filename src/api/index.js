import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

export const fetchTeams = async () => {
  try {
    const teams = await axios.get(`${url}/teams/by/elo_recent`);
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeams_byRegion = async (region) => {
  try {
    const teams = await axios.get(`${url}/teams/region/${region}/by/elo_recent`);
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
}

export const fetchTeams_byDistrict = async (district) => {
  try {
    const teams = await axios.get(`${url}/teams/district/${district}/by/elo_recent`);
    console.log(teams.data);
    return teams.data;
  } catch (error) {
    return error;
  }
}
