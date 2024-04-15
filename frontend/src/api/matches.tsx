import { CURR_YEAR } from "../constants";
import query from "./storage";

export async function getNoteworthyMatches(
  year: number,
  location: string | null,
  elim: string | null,
  week: number | null
) {
  let suffix = `/noteworthy_matches/${year}`;
  let storageKey = `noteworthy_matches_${year}`;
  if (location) {
    suffix += `?${location.replace("_", "=")}`;
    storageKey += `_${location}`;
  }
  if (elim) {
    suffix += `&elim=${elim}`;
    storageKey += `_${elim}`;
  }
  if (week) {
    suffix += `&week=${week}`;
    storageKey += `_${week}`;
  }

  return query(storageKey, suffix, 0, 60, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}

export async function getUpcomingMatches(
  location: string | null,
  elim: string | null,
  filterMatches: string | null,
  sortMatches: string
) {
  let suffix = `/upcoming_matches?limit=20&metric=${sortMatches}`;
  let storageKey = `upcoming_matches_${sortMatches}`;
  if (filterMatches) {
    suffix += `&minutes=${filterMatches}`;
    storageKey += `_${filterMatches}`;
  }
  if (location) {
    suffix += `&${location.replace("_", "=")}`;
    storageKey += `_${location}`;
  }
  if (elim) {
    suffix += `&elim=${elim}`;
    storageKey += `_${elim}`;
  }
  return query(storageKey, suffix, 0, 60, 60); // 1 minute
}
