import axios from 'axios';

const url = 'https://backend.statbotics.io/api';

export const fetchTeams = async () => {
  try {
    const teams = await axios.get(`${url}/teams/?limit=10000`);
    console.log(teams.data)
    return teams.data;
  } catch (error) {
    return error;
  }
};

export const fetchTeam = async () => {
  try {
    const team = await axios.get(`${url}/team_matches/team/5511`);
    console.log(team.data)
    return team.data;
  } catch (error) {
    return error;
  }
};
