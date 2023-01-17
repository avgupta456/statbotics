import {
  APIMatch,
  APITeam,
  APITeamEvent,
  APITeamMatch,
  APITeamYear,
  APIYear,
} from "../../../../components/types/api";

export type TeamData = APITeam;

export type TeamYearData = {
  year: APIYear;
  team_year: APITeamYear;
  team_events: APITeamEvent[];
  matches: APIMatch[];
  team_matches: APITeamMatch[];
};

export type TeamYearsData = {
  team: number;
  year: number;
  epa_rank: number;
  epa_count: number;
}[];
