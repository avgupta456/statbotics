import { Match, TeamEvent, TeamMatch, YearStats } from "../../../../components/types/api";

export type Data = {
  event_name: string;
  year: number;
  team_events: TeamEvent[];
  matches: Match[];
  team_matches: TeamMatch[];
  year_stats: YearStats;
};
