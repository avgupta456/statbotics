import { APITeamMatch } from "../types/api";
import { EventData } from "../types/data";
import query from "./storage";

export async function getEvent(event: string): Promise<EventData> {
  const urlSuffix = `/event/${event}`;
  const storageKey = `event_${event}_v3`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}

export async function getTeamEventTeamMatches(
  team: string,
  event: string
): Promise<APITeamMatch[]> {
  const urlSuffix = `/event/${event}/team_matches/${team}`;
  const storageKey = `event_${event}_team_matches_${team}_v3`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}
