import { MatchData } from "../types/data";
import query, { version } from "./storage";

export async function getMatch(match: string): Promise<MatchData> {
  const urlSuffix = `/match/${match}`;
  const storageKey = `match_${match}_${version}`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}
