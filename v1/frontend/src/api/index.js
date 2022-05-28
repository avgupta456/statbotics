import { BACKEND_URL } from "../constants";

export const url = BACKEND_URL;

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
  fetchTeam_Years,
  fetchTeamYearElo,
} from "./team_year_api.js";

export {
  fetchEvents_Simple,
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

export {
  fetchTeamEvents,
  fetchTeamEvents_Team,
  fetchTeamEvents_TeamYear,
} from "./team_event_api.js";

export { fetchMatches_Event } from "./match_api.js";

export { fetchRankings } from "./tba_api.js";

export { fetchSimFull, fetchSimIndex } from "./event_sim_api.js";
