import {
  APIEvent,
  APIMatch,
  APITeam,
  APITeamEvent,
  APITeamMatch,
  APITeamYear,
  APIYear,
  emptyAPIYear,
} from "./api";

export type TeamYearsData = {
  year: APIYear;
  team_years: APITeamYear[];
};

export const emptyTeamYearsData: TeamYearsData = {
  year: emptyAPIYear,
  team_years: [],
};

export type TeamYearData = {
  year: APIYear;
  team: APITeam;
  team_year: APITeamYear;
  team_events: APITeamEvent[];
  matches: APIMatch[];
  team_matches: APITeamMatch[];
};

export type TeamYearRedirect = {
  year: APIYear;
  team_active_years: {
    rookie_year: number;
    last_active_year: number;
  };
};

export type EventsData = {
  year: APIYear;
  events: APIEvent[];
};

export const emptyEventData: EventsData = {
  year: emptyAPIYear,
  events: [],
};

export type EventData = {
  event: APIEvent;
  matches: APIMatch[];
  team_events: APITeamEvent[];
  team_matches: APITeamMatch[];
  year: APIYear;
};

export type MatchData = {
  year: APIYear;
  event: APIEvent;
  team_events: APITeamEvent[];
  match: APIMatch;
  team_matches: APITeamMatch[];
};

export type ShortTeam = {
  team: string;
  name: string;
  active: boolean;
};

export type ShortEvent = {
  key: string;
  name: string;
};
