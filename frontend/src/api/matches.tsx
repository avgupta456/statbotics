import { CURR_YEAR } from "../constants";
import query, { version } from "./storage";

export async function getNoteworthyMatches(
  year: number,
  country: string | null,
  state: string | null,
  district: string | null,
  elim: string | null,
  week: number | null
) {
  let suffix = `/noteworthy_matches/${year}`;
  let storageKey = `noteworthy_matches_${year}_${version}`;

  let suffixes = [];
  if (country) {
    suffixes.push(`country=${country}`);
    storageKey += `_${country}`;
  }
  if (state) {
    suffixes.push(`state=${state}`);
    storageKey += `_${state}`;
  }
  if (district) {
    suffixes.push(`district=${district}`);
    storageKey += `_${district}`;
  }
  if (elim) {
    suffixes.push(`elim=${elim}`);
    storageKey += `_${elim}`;
  }
  if (week) {
    suffixes.push(`week=${week}`);
    storageKey += `_${week}`;
  }

  suffix += suffixes.length > 0 ? `?${suffixes.join("&")}` : "";

  return query(storageKey, suffix, 0, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}

export async function getUpcomingMatches(
  country: string | null,
  state: string | null,
  district: string | null,
  elim: string | null,
  filterMatches: string | null,
  sortMatches: string
) {
  let suffix = `/upcoming_matches?limit=20&metric=${sortMatches}`;
  let storageKey = `upcoming_matches_${sortMatches}_${version}`;
  if (filterMatches) {
    suffix += `&minutes=${filterMatches}`;
    storageKey += `_${filterMatches}`;
  }
  if (country) {
    suffix += `&country=${country}`;
    storageKey += `_${country}`;
  }
  if (state) {
    suffix += `&state=${state}`;
    storageKey += `_${state}`;
  }
  if (district) {
    suffix += `&district=${district}`;
    storageKey += `_${district}`;
  }
  if (elim) {
    suffix += `&elim=${elim}`;
    storageKey += `_${elim}`;
  }
  return query(storageKey, suffix, 0, 60); // 1 minute
}
