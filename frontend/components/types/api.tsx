export type APITeam = {
  num: number;
  team: string;
  state?: string;
  country?: string;
  district?: string;
  rookie_year: number;
  offseason: boolean;
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

export type APIYear = {
  year: number;
  total_stats: PercentileStats;
  auto_stats: PercentileStats;
  teleop_stats: PercentileStats;
  endgame_stats: PercentileStats;
  rp_1_stats: PercentileStats;
  rp_2_stats: PercentileStats;
  foul_rate: number;
};

export const emptyAPIYear: APIYear = {
  year: 0,
  total_stats: emptyPercentileStats,
  auto_stats: emptyPercentileStats,
  teleop_stats: emptyPercentileStats,
  endgame_stats: emptyPercentileStats,
  rp_1_stats: emptyPercentileStats,
  rp_2_stats: emptyPercentileStats,
  foul_rate: 0,
};

export type APITeamYear = {
  num: number;
  team: string;
  state?: string;
  country?: string;
  district?: string;
  epa_rank: number;
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
  offseason: boolean;
};

export type APIEvent = {
  event_name: string;
  year: number;
};

export type APITeamEvent = {
  num: number;
  team: string;
  start_total_epa: number;
  start_rp_1_epa: number;
  start_rp_2_epa: number;
  total_epa: number;
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
};

export type APIMatch = {
  year: number;
  event: string;
  time: number;
  key: string;
  match_name: string;
  video?: string;
  comp_level: string;
  set_number: number;
  match_number: number;
  playoff: boolean;
  red: number[];
  blue: number[];

  red_score: number;
  red_auto: number;
  red_teleop: number;
  red_endgame: number;
  red_1: number;
  red_2: number;
  red_fouls: number;
  red_rp_1: number;
  red_rp_2: number;
  blue_score: number;
  blue_auto: number;
  blue_teleop: number;
  blue_endgame: number;
  blue_1: number;
  blue_2: number;
  blue_fouls: number;
  blue_rp_1: number;
  blue_rp_2: number;
  winner: string;

  red_epa_pred: number;
  red_auto_epa_pred: number;
  red_teleop_epa_pred: number;
  red_endgame_epa_pred: number;
  red_rp_1_pred: number;
  red_rp_2_pred: number;
  blue_epa_pred: number;
  blue_auto_epa_pred: number;
  blue_teleop_epa_pred: number;
  blue_endgame_epa_pred: number;
  blue_rp_1_pred: number;
  blue_rp_2_pred: number;
  epa_win_prob: number;
  pred_winner: string;
};

export type APITeamMatch = {
  num: number;
  alliance: string;
  match: string;
  time: number;
  playoff: boolean;
  match_number: number; // quals only
  total_epa: number;
  auto_epa: number;
  teleop_epa: number;
  endgame_epa: number;
  rp_1_epa: number;
  rp_2_epa: number;
  offseason: boolean;
};
