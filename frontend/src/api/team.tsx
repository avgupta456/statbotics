import { BUCKET_URL, CURR_YEAR } from "../constants";
import { APIMatch, APITeam, APITeamEvent, APITeamMatch, APITeamYear, APIYear } from "../types/api";
import { getEvent } from "./event";
import query, { decompress, version } from "./storage";
import { getYearTeamYears } from "./teams";

export async function getTeam(team: number): Promise<{ team: APITeam; team_years: any[] }> {
  const urlSuffix = `/team/${team}`;
  const storageKey = `team_${team}_${version}`;

  return query(storageKey, urlSuffix, false, 0, 60); // 1 minute
}

export async function getTeamYear(
  team: number,
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

  const readBucket = async (url: string) => {
    const res = await fetch(url, {
      next: { revalidate: 0 },
    });
    if (res.ok) {
      const buffer = await res.arrayBuffer();
      const data = decompress(buffer);
      return data;
    } else {
      throw new Error(`Failed to fetch from bucket: ${res.status}`);
    }
  };

  try {
    // try to reconstruct output from team, team_to_events, and events
    if (year !== CURR_YEAR) {
      throw new Error("Not current year");
    }
    const teamToEvents: {
      [key: number]: string[];
    } = await readBucket(`${BUCKET_URL}/team_to_events`);
    const teamYearData = await getYearTeamYears(year);
    const teamYear = teamYearData?.team_years?.find((teamYear) => teamYear.team === team);
    const events = await Promise.all(
      teamToEvents[team].map(async (eventKey) => await getEvent(eventKey))
    );
    const matches = events.flatMap((event) =>
      event.matches
        .filter(
          (match) =>
            match.alliances.red.team_keys.includes(team) ||
            match.alliances.blue.team_keys.includes(team)
        )
        .sort((a, b) => a.time - b.time)
    );
    const teamMatches = events
      .flatMap((event) => event.team_matches.filter((match) => match.team === team))
      .sort((a, b) => a.time - b.time);
    const getEarliestMatch = (teamEvent: APITeamEvent) =>
      matches
        .filter((match) => match.event === teamEvent.event)
        .map((match) => match.time)
        .sort((a, b) => a - b)[0];
    const teamEvents = events
      .map((event) => event.team_events.find((e) => e.team === team))
      .sort((a, b) => {
        const aTime = getEarliestMatch(a);
        const bTime = getEarliestMatch(b);
        if (a.week !== b.week) {
          return a.week - b.week;
        } else if (aTime !== bTime) {
          return aTime - bTime;
        } else {
          return a.time - b.time;
        }
      });
    return {
      year: teamYearData.year,
      team_year: teamYear,
      team_events: teamEvents,
      matches,
      team_matches: teamMatches,
    };
  } catch (e) {
    return query(storageKey, urlSuffix, false, 0, year === CURR_YEAR ? 60 : 60 * 60); // 1 minute / 1 hour
  }
}

export async function getTeamYears(team: number): Promise<any[]> {
  const urlSuffix = `/team/${team}/years`;
  const storageKey = `team_${team}_years_${version}`;

  return query(storageKey, urlSuffix, false, 0, 60); // 1 minute
}
