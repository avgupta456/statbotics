import { BACKEND_URL, CURR_YEAR } from "../utils/constants";
import { getWithExpiry, setWithExpiry } from "../utils/localStorage";
import { log, round } from "../utils/utils";

export default async function getTeamYearData(year: number, limit?: number | null) {
  let urlSuffix = `/team_years/${year}`;
  let storageKey = `team_years_${year}`;
  if (limit) {
    urlSuffix += `?limit=${limit}&metric=epa`;
    storageKey += `_${limit}`;
  }

  const cacheData = getWithExpiry(storageKey);
  if (cacheData && cacheData?.team_years?.length > 0) {
    log(`Used Local Storage: ${storageKey}`);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}${urlSuffix}`, { next: { revalidate: 60 } });
  log(`${urlSuffix} took ${round(performance.now() - start, 0)}ms`);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(storageKey, data, expiry);
  return data;
}
