export const url = "https://backend.statbotics.io/api";
//export const url = 'http://localhost:8000/api';

export {
  fetchTeams_Simple,
  fetchTeams,
  fetchTeams_byCountry,
  fetchTeams_byState,
  fetchTeams_byDistrict,
  fetchTeam,
} from "./team_api.js";

export {
  fetchTeamsYear,
  fetchTeamsYear_byCountry,
  fetchTeamsYear_byState,
  fetchTeamsYear_byDistrict,
  fetchTeamYearElo,
} from "./team_year_api.js";

export {
  fetchEvents,
  fetchEvents_byWeek,
  fetchEvents_byCountry,
  fetchEvents_byCountryWeek,
  fetchEvents_byState,
  fetchEvents_byStateWeek,
  fetchEvents_byDistrict,
  fetchEvents_byDistrictWeek,
  fetchEvent,
} from "./event_api.js";
