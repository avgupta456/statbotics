import { CURR_YEAR } from "../utils/constants";
import query from "./storage";

export async function getTeamYearData(year: number, limit?: number | null) {
  let urlSuffix = `/team_years/${year}`;
  let storageKey = `team_years_${year}`;
  if (limit) {
    urlSuffix += `?limit=${limit}&metric=epa`;
    storageKey += `_${limit}`;
  }
  storageKey += "_v3";

  return query(storageKey, urlSuffix, 0, 60, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}

export async function getTeamYearMatches(year: number, teamNum: string) {
  const urlSuffix = `/team_year/${year}/${teamNum}/matches`;
  const storageKey = `team_year_matches_${year}_${teamNum}`;

  return query(storageKey, urlSuffix, 0, 60, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}
