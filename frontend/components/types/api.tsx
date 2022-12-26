export type TeamEvent = {
  num: number;
  team: string;
  total_epa: number;
  // total_epa_diff: number;
  auto_epa: number;
  // auto_epa_diff: number;
  teleop_epa: number;
  // teleop_epa_diff: number;
  endgame_epa: number;
  // endgame_epa_diff: number;
  rp_1_epa: number;
  // rp_1_epa_diff: number;
  rp_2_epa: number;
  // rp_2_epa_diff: number;
  wins: number;
  losses: number;
  ties: number;
  count: number;
  rank: number;
};

export type TeamYear = {
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

export type PercentileStats = {
  p99: number;
  p95: number;
  p90: number;
  p75: number;
  p50: number;
  p25: number;
  mean: number;
  sd: number;
};

export type YearStats = {
  total: PercentileStats;
  auto: PercentileStats;
  teleop: PercentileStats;
  endgame: PercentileStats;
  rp_1: PercentileStats;
  rp_2: PercentileStats;
  foul_rate: number;
};
