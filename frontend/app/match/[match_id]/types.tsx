type Match = {
  key: string;
  event: string;
  red: [string, string, string];
  blue: [string, string, string];
  epa_win_prob: number;
  red_auto: number;
  blue_auto: number;
  red_teleop: number;
  blue_teleop: number;
  red_endgame: number;
  blue_endgame: number;
  red_fouls: number;
  blue_fouls: number;
  red_rp_1: number;
  blue_rp_1: number;
  red_rp_2: number;
  blue_rp_2: number;
  red_score: number;
  blue_score: number;
  red_auto_epa_sum: number;
  blue_auto_epa_sum: number;
  red_teleop_epa_sum: number;
  blue_teleop_epa_sum: number;
  red_endgame_epa_sum: number;
  blue_endgame_epa_sum: number;
  red_epa_sum: number;
  blue_epa_sum: number;
  epa_winner: string;
  winner: string;
  video: string;
};

type TeamMatch = {
  key: string;
  team: string;
  auto_epa: number;
  teleop_epa: number;
  endgame_epa: number;
  epa: number;
};

type TeamMatches = {
  [team: string]: TeamMatch;
};

type YearStats = {
  auto_mean: number;
  teleop_mean: number;
  endgame_mean: number;
  total_mean: number;
};

export type Data = {
  match: Match;
  team_matches: TeamMatches;
  year_stats: YearStats;
  event_name: string;
  match_name: string;
};
