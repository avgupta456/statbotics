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
  score_mean: number;
  score_sd: number;
  total_stats: PercentileStats;
  auto_stats: PercentileStats;
  teleop_stats: PercentileStats;
  endgame_stats: PercentileStats;
  rp_1_stats: PercentileStats;
  rp_2_stats: PercentileStats;
};

export const emptyAPIYear: APIYear = {
  year: 0,
  score_mean: 0,
  score_sd: 1,
  total_stats: emptyPercentileStats,
  auto_stats: emptyPercentileStats,
  teleop_stats: emptyPercentileStats,
  endgame_stats: emptyPercentileStats,
  rp_1_stats: emptyPercentileStats,
  rp_2_stats: emptyPercentileStats,
};

export type APITeamYear = {
  year: number;
  num: number;
  team: string;
  state?: string;
  country?: string;
  district?: string;
  is_competing?: boolean;
  next_event_key?: string;
  next_event_name?: string;
  next_event_week?: number;
  epa_rank: number;
  epa_count: number;
  state_epa_rank: number;
  state_epa_count: number;
  country_epa_rank: number;
  country_epa_count: number;
  district_epa_rank: number;
  district_epa_count: number;
  total_epa: number;
  unitless_epa: number;
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
  offseason: boolean;
};

export type APIEvent = {
  key: string;
  name: string;
  year: number;
  week: number;
  start_date: string;
  end_date: string;
  country?: string;
  state?: string;
  district?: string;
  offseason: boolean;
  status: string;
  status_str: string;
  qual_matches: number;
  current_match: number;
  epa_acc?: number;
  epa_mse?: number;
  epa_max?: number;
  epa_top8?: number;
  epa_top24?: number;
  epa_mean?: number;
};

export type APITeamEvent = {
  num: number;
  team: string;
  event: string;
  event_name: string;
  week: number;
  time: number;
  first_event: boolean;
  num_teams: number;
  start_total_epa: number;
  start_rp_1_epa: number;
  start_rp_2_epa: number;
  total_epa: number;
  unitless_epa: number;
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
  qual_wins: number;
  qual_losses: number;
  qual_ties: number;
  qual_count: number;
  rank: number;
  rps: number;
  rps_per_match: number;
  offseason: boolean;
};

export type APIMatch = {
  year: number;
  event: string;
  time: number;
  predicted_time: number;
  key: string;
  match_name: string;
  status: string;
  video?: string;
  comp_level: string;
  set_number: number;
  match_number: number;
  playoff: boolean;
  red: number[];
  blue: number[];
  red_surrogates: number[];
  blue_surrogates: number[];
  red_dqs: number[];
  blue_dqs: number[];

  red_score: number;
  red_auto: number;
  red_teleop: number;
  red_endgame: number;
  red_1: number;
  red_2: number;
  red_fouls: number;
  red_rp_1: number;
  red_rp_2: number;
  red_tiebreaker: number;
  blue_score: number;
  blue_auto: number;
  blue_teleop: number;
  blue_endgame: number;
  blue_1: number;
  blue_2: number;
  blue_fouls: number;
  blue_rp_1: number;
  blue_rp_2: number;
  blue_tiebreaker: number;
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
  post_epa?: number;
  offseason: boolean;
  status: string;
};
