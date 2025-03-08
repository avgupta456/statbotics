import { APITeamMatch } from "../types/api";
import { EventData } from "../types/data";
import query, { version } from "./storage";

export async function getEvent(event: string): Promise<EventData> {
  const urlSuffix = `/event/${event}`;
  const storageKey = `event_${event}_${version}`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}

export async function getTeamEventTeamMatches(
  team: number,
  event: string
): Promise<APITeamMatch[]> {
  const urlSuffix = `/event/${event}/team_matches/${team}`;
  const storageKey = `event_${event}_team_matches_${team}_${version}`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}
