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

export type SummaryRow = {
  team: number;
  year: number;
  norm_epa: number;
  epa_rank?: number;
  epa_percentile?: number;
  country_epa_rank?: number;
  country_epa_percentile?: number;
  district_epa_rank?: number;
  district_epa_percentile?: number;
  state_epa_rank?: number;
  state_epa_percentile?: number;
};

export type TeamYearsData = SummaryRow[];
