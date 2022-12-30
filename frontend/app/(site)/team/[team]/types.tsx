import { Match, TeamMatch } from "../../../../components/types/api";

export type TeamData = {
  num: number;
  team: string;
  country: string;
  state: string;
  district: string;
  rookie_year: number;
};

export type TeamYearData = {
  num: number;
  team: string;
  year: number;
  team_year: {
    epa_rank: number;
    epa_count: number;
    country_epa_rank: number;
    country_count: number;
    state_epa_rank: number;
    state_count: number;
    district_epa_rank: number;
    district_count: number;
    wins: number;
    losses: number;
    ties: number;
    count: number;
    epa: number;
    auto_epa: number;
    teleop_epa: number;
    endgame_epa: number;
    rp_1_epa: number;
    rp_2_epa: number;
    foul_rate: number;
  };
  team_events: {
    event: string;
    event_name: string;
    week: number;
    epa: number;
    norm_epa: number;
    auto_epa: number;
    teleop_epa: number;
    endgame_epa: number;
    rp_1_epa: number;
    rp_2_epa: number;
    wins: number;
    losses: number;
    ties: number;
    count: number;
    rank: number;
    num_teams: number;
    matches: Match[];
  }[];
  team_matches: TeamMatch[];
};
