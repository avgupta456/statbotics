import { APIShortEvent, APIShortTeam } from "../types/api";
import query from "./storage";

export async function getAllTeams(): Promise<APIShortTeam[]> {
  return query("full_team_list_v3", "/teams/all", 1000, 60 * 60 * 24 * 7); // 1 week expiry
}

export async function getAllEvents(): Promise<APIShortEvent[]> {
  return query("full_event_list_v3", "/events/all", 1000, 60 * 60 * 24 * 7); // 1 week expiry
}
