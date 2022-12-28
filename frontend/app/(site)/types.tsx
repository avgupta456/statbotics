import { TeamYear, YearStats, emptyYearStats } from "../../components/types/api";

export type Data = {
  team_years: TeamYear[];
  year_stats: YearStats;
};

export const emptyData: Data = {
  team_years: [],
  year_stats: emptyYearStats,
};
