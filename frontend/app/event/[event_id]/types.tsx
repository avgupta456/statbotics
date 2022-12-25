import { YearStats } from "../../../components/types/api";

type TeamEvent = {
  num: number;
  team: string;
  epa_start: number;
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
  rank: number;
};

export type Data = {
  event_name: string;
  team_events: TeamEvent[];
  year_stats: YearStats;
};
