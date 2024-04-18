import { MatchData } from "../types/data";
import query from "./storage";

export async function getMatch(match: string): Promise<MatchData> {
  const urlSuffix = `/match/${match}`;
  const storageKey = `match_${match}_v3`;

  return query(storageKey, urlSuffix, 0, 60); // 1 minute
}
