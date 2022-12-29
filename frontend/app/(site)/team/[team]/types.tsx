import { TeamMatch } from "../../../../components/types/api";

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
  };
  team_events: {
    event: string;
    event_name: string;
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
    matches: {
      comp_level: string;
      set_number: number;
      match_number: number;
      alliance: string;
      red: number[];
      blue: number[];
      red_score: number;
      blue_score: number;
      red_rp_1: number;
      red_rp_2: number;
      blue_rp_1: number;
      blue_rp_2: number;
    }[];
  }[];
  team_matches: TeamMatch[];
};
