import { BACKEND_URL } from "../utils/constants";
import { getWithExpiry, setWithExpiry } from "../utils/localStorage";
import { log, round } from "../utils/utils";

export async function getTeamData() {
  const cacheData = getWithExpiry("full_team_list");
  if (cacheData && cacheData?.length > 1000) {
    log("Used Local Storage: Full Team List");
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/teams/all`, { next: { revalidate: 60 } });
  log(`/teams/all took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  setWithExpiry("full_team_list", data, 60 * 60 * 24 * 7); // 1 week expiry
  return data;
}

export async function getEventData() {
  const cacheData = getWithExpiry("full_event_list");
  if (cacheData && cacheData?.length > 1000) {
    log("Used Local Storage: Full Event List");
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/events/all`, { next: { revalidate: 60 } });
  log(`events/all took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  setWithExpiry("full_event_list", data, 60 * 60 * 24 * 7); // 1 week expiry
  return data;
}
