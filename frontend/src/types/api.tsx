export type EPAPercentiles = {
  p99: number;
  p90: number;
  p75: number;
  p25: number;
};

export type WinProbMetrics = {
  count: number;
  conf?: number;
  acc?: number;
  mse?: number;
};

export type ScorePredMetrics = {
  count: number;
  rmse?: number;
  error?: number;
};

export type RPPredMetrics = {
  error?: number;
  acc?: number;
};

export type APIYear = {
  year: number;
  score_mean: number;
  score_sd: number;
  percentiles: {
    [key: string]: EPAPercentiles;
  };
  breakdown: {
    [key: string]: number;
  };
  metrics: {
    win_prob: {
      season: WinProbMetrics;
      champs: WinProbMetrics;
    };
    score_pred: {
      season: ScorePredMetrics;
      champs: ScorePredMetrics;
    };
    rp_pred: {
      season: {
        count: any; // number
        [key: string]: RPPredMetrics;
      };
      champs: {
        count: any; // number
        [key: string]: RPPredMetrics;
      };
    };
  };
};

export const emptyAPIYear: APIYear = {
  year: 0,
  score_mean: 0,
  score_sd: 0,
  percentiles: {},
  breakdown: {},
  metrics: {
    win_prob: {
      season: {
        count: 0,
      },
      champs: {
        count: 0,
      },
    },
    score_pred: {
      season: {
        count: 0,
      },
      champs: {
        count: 0,
      },
    },
    rp_pred: {
      season: {
        count: {},
      },
      champs: {
        count: {},
      },
    },
  },
};

export type Record = {
  wins: number;
  losses: number;
  ties: number;
  count: number;
  winrate: number;
};

export type APITeam = {
  team: number;
  name: string;
  country: string;
  state?: string;
  district?: string;
  rookie_year: number;
  active: boolean;
  record: {
    season: Record;
    full: Record;
  };
  norm_epa: {
    current: number;
    recent: number;
    mean: number;
    max: number;
  };
};

export type EPARank = {
  rank: number;
  percentile: number;
  team_count: number;
};

export type APITeamYear = {
  team: number;
  year: number;
  name: string;
  country: string;
  state?: string;
  district?: string;
  rookie_year: number;
  epa: {
    total_points: { mean: number; sd: number };
    unitless: number;
    norm: number;
    conf: [number, number];
    breakdown: { [key: string]: number };
    stats: { start: number; pre_champs: number; max: number };
    ranks: {
      total: EPARank;
      country: EPARank;
      state?: EPARank;
      district?: EPARank;
    };
  };
  record: Record;
  district_points?: number;
  district_rank?: number;
  competing?: {
    this_week: boolean;
    next_event_key: string;
    next_event_name: string;
    next_event_week: number;
  };
};

export type APIEvent = {
  key: string;
  year: number;
  name: string;
  time: number;
  country: string;
  state?: string;
  district?: string;
  start_date: string;
  end_date: string;
  type: string;
  week: number;
  video?: string;
  status: string;
  status_str: string;
  num_teams: number;
  current_match: number;
  qual_matches: number;
  epa: {
    max?: number;
    top_8?: number;
    top_24?: number;
    mean?: number;
    sd?: number;
  };
  metrics: {
    win_prob: WinProbMetrics;
    score_pred: ScorePredMetrics;
    rp_pred: {
      count: any; // number
      [key: string]: RPPredMetrics;
    };
  };
};

export type APITeamEvent = {
  team: number;
  year: number;
  event: string;
  time: number;
  team_name: string;
  event_name: string;
  country: string;
  state?: string;
  district?: string;
  type: string;
  week: number;
  status: string;
  first_event: boolean;
  epa: {
    total_points: { mean: number; sd: number };
    unitless: number;
    norm: number;
    conf: [number, number];
    breakdown: { [key: string]: number };
    stats: { start: number; pre_elim: number; mean: number; max: number };
  };
  record: {
    qual: {
      wins: number;
      losses: number;
      ties: number;
      count: number;
      winrate: number;
      rps: number;
      rps_per_match: number;
      rank: number;
      num_teams: number;
    };
    elim: {
      wins: number;
      losses: number;
      ties: number;
      count: number;
      winrate: number;
      alliance?: string;
      is_captain: boolean;
    };
    total: {
      wins: number;
      losses: number;
      ties: number;
      count: number;
      winrate: number;
    };
  };
};

export type APIMatch = {
  key: string;
  year: number;
  event: string;
  week: number;
  elim: boolean;
  comp_level: string;
  set_number: number;
  match_number: number;
  match_name: string;
  time: number;
  predicted_time: number;
  status: string;
  video?: string;
  alliances: {
    red: {
      team_keys: number[];
      surrogate_team_keys: number[];
      dq_team_keys: number[];
    };
    blue: {
      team_keys: number[];
      surrogate_team_keys: number[];
      dq_team_keys: number[];
    };
  };
  pred: {
    winner: string;
    red_win_prob: number;
    red_score: number;
    blue_score: number;
    [key: string]: any; // number
  };
  result: {
    winner: string;
    red_score: number;
    blue_score: number;
    red_no_foul: number;
    blue_no_foul: number;
    [key: string]: any; // boolean
  };
};

export type APITeamMatch = {
  team: number;
  match: string;
  year: number;
  event: string;
  alliance: string;
  time: number;
  week: number;
  elim: boolean;
  dq: boolean;
  surrogate: boolean;
  status: string;
  epa: {
    post: number;
    breakdown: { [key: string]: number };
  };
};

export type APIShortTeam = {
  team: string;
  name: string;
  active: boolean;
};

export type APIShortEvent = {
  key: string;
  name: string;
};
