import { CURR_YEAR } from "../constants";
import { APIMatch, APITeam, APITeamEvent, APITeamMatch, APITeamYear, APIYear } from "../types/api";
import query, { version } from "./storage";

export async function getTeam(team: string): Promise<{ team: APITeam; team_years: any[] }> {
  const urlSuffix = `/team/${team}`;
  const storageKey = `team_${team}_${version}`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}

export async function getTeamYear(
  team: string,
  year: number
): Promise<{
  year: APIYear;
  team_year: APITeamYear;
  team_events: APITeamEvent[];
  matches: APIMatch[];
  team_matches: APITeamMatch[];
}> {
  const urlSuffix = `/team/${team}/${year}`;
  const storageKey = `team_${team}_${year}_${version}`;

  return query(storageKey, urlSuffix, 0, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}

export async function getTeamYears(team: string): Promise<any[]> {
  const urlSuffix = `/team/${team}/years`;
  const storageKey = `team_${team}_years_${version}`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}
