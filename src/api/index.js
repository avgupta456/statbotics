import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

export const fetchTeams = async () => {
  try {
    const teams = await axios.get(`${url}/teams/by/elo_recent`);
    console.log(teams.data)
    return teams.data;
  } catch (error) {
    return error;
  }
};
