import { TeamEvent, YearStats } from "../../../../components/types/api";

export type Data = {
  event_name: string;
  year: number;
  team_events: TeamEvent[];
  year_stats: YearStats;
};
