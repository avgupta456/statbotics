export type TeamEvent = {
  num: number;
  team: string;
  // For simulation initialization
  start_total_epa: number;
  start_rp_1_epa: number;
  start_rp_2_epa: number;
  // For tables and figures
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

export type TeamYear = {
  num: number;
  team: string;
  state: string;
  country: string;
  district: string;
  norm_epa: number;
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

export type Match = {
  key: string;
  comp_level: string;
  set_number: number;
  match_number: number;
  playoff: boolean;
  alliance: string;
  red: number[];
  blue: number[];
  red_score: number;
  blue_score: number;
  winner: string;
  red_rp_1: number;
  red_rp_2: number;
  blue_rp_1: number;
  blue_rp_2: number;
  red_epa_pred: number;
  blue_epa_pred: number;
  epa_win_prob: number;
  pred_winner: string;
  red_rp_1_pred: number;
  red_rp_2_pred: number;
  blue_rp_1_pred: number;
  blue_rp_2_pred: number;
  // for simulation
  red_auto: number;
  red_teleop: number;
  red_endgame: number;
  red_1: number;
  red_2: number;
  blue_auto: number;
  blue_teleop: number;
  blue_endgame: number;
  blue_1: number;
  blue_2: number;
};

export type TeamMatch = {
  team: number;
  match: string;
  alliance: string;
  match_num: number;
  label: string;
  time: number;
  playoff: boolean;
  norm_epa: number;
  total_epa: number;
  auto_epa: number;
  teleop_epa: number;
  endgame_epa: number;
  rp_1_epa: number;
  rp_2_epa: number;
};

// Percentile/Year Stats

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

export const emptyPercentileStats: PercentileStats = {
  p99: 0,
  p95: 0,
  p90: 0,
  p75: 0,
  p50: 0,
  p25: 0,
  mean: 0,
  sd: 0,
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

export const emptyYearStats: YearStats = {
  total: emptyPercentileStats,
  auto: emptyPercentileStats,
  teleop: emptyPercentileStats,
  endgame: emptyPercentileStats,
  rp_1: emptyPercentileStats,
  rp_2: emptyPercentileStats,
  foul_rate: 0,
};
