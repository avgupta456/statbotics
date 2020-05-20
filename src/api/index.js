import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

export const fetchTeams = async () => {
  try {
    const teams = await axios.get(`${url}/teams/?limit=1000`);
    console.log(teams.data)
    return teams.data;
  } catch (error) {
    return error;
  }
};
