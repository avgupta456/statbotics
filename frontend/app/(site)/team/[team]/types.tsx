import { TeamMatch } from "../../../../components/types/api";

export type TeamData = {
  num: number;
  team: string;
  rookie_year: number;
};

export const emptyTeamData: TeamData = {
  num: 0,
  team: "",
  rookie_year: 2002,
};

export type TeamYearData = {
  num: number;
  year: number;
  team_year: {
    epa_rank: number;
    country_epa_rank: number;
    state_epa_rank: number;
    district_epa_rank: number;
    epa: number;
    auto_epa: number;
    teleop_epa: number;
    endgame_epa: number;
    rp_1_epa: number;
    rp_2_epa: number;
  };
  matches: TeamMatch[];
};

export const emptyTeamYearData: TeamYearData = {
  num: 0,
  year: 0,
  team_year: {
    epa_rank: 0,
    country_epa_rank: 0,
    state_epa_rank: 0,
    district_epa_rank: 0,
    epa: 0,
    auto_epa: 0,
    teleop_epa: 0,
    endgame_epa: 0,
    rp_1_epa: 0,
    rp_2_epa: 0,
  },
  matches: [],
};
