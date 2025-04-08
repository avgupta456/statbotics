import { CURR_YEAR } from "../constants";
import { APIEvent, APIYear } from "../types/api";
import query, { version } from "./storage";

// eslint-disable-next-line import/prefer-default-export
export async function getYearEvents(year: number): Promise<{ year: APIYear; events: APIEvent[] }> {
  const urlSuffix = `/events/${year}`;
  const storageKey = `events_${year}_${version}`;
  return query(storageKey, urlSuffix, year === CURR_YEAR, 0, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}
