import { YearStats } from "../../../components/types/api";

type TeamYear = {
  num: number;
  name: string;
  state: string;
  country: string;
  district: string;
  total_epa: number;
  auto_epa: number;
  teleop_epa: number;
  endgame_epa: number;
  rp_1_epa: number;
  rp_2_epa: number;
  wins: number;
  losses: number;
  ties: number;
  count: number;
};

export type Data = {
  team_years: TeamYear[];
  year_stats: YearStats;
};
