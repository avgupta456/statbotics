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
