import { Match, TeamEvent, YearStats } from "../../../../components/types/api";

export type Data = {
  event_name: string;
  year: number;
  team_events: TeamEvent[];
  matches: Match[];
  year_stats: YearStats;
};
