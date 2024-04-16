export type SummaryRow = {
  team: number;
  year: number;
  norm_epa: number;
  unitless_epa: number;
  epa_rank?: number;
  epa_percentile?: number;
  country_epa_rank?: number;
  country_epa_percentile?: number;
  district_epa_rank?: number;
  district_epa_percentile?: number;
  state_epa_rank?: number;
  state_epa_percentile?: number;
};
