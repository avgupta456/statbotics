import { APIEvent, APIYear } from "../types/api";
import { CURR_YEAR } from "../utils/constants";
import query from "./storage";

// eslint-disable-next-line import/prefer-default-export
export async function getYearEvents(year: number): Promise<{ year: APIYear; events: APIEvent[] }> {
  const urlSuffix = `/events/${year}`;
  const storageKey = `events_${year}_v3`;
  return query(storageKey, urlSuffix, 0, 60, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
}
