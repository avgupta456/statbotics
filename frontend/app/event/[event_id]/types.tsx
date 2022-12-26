import { TeamEvent, YearStats } from "../../../components/types/api";

export type Data = {
  event_name: string;
  team_events: TeamEvent[];
  year_stats: YearStats;
};
