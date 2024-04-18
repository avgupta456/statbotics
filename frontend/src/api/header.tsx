import { APIShortEvent, APIShortTeam } from "../types/api";
import query, { version } from "./storage";

export async function getAllTeams(): Promise<APIShortTeam[]> {
  return query(`full_team_list_${version}`, "/teams/all", 1000, 60 * 60 * 24 * 7); // 1 week expiry
}

export async function getAllEvents(): Promise<APIShortEvent[]> {
  return query(`full_event_list_${version}`, "/events/all", 1000, 60 * 60 * 24 * 7); // 1 week expiry
}
