import { APIEvent, APITeamYear, APIYear, emptyAPIYear } from "./api";

export type TeamYearsData = {
  year: APIYear;
  team_years: APITeamYear[];
};

export const emptyTeamYearsData: TeamYearsData = {
  year: emptyAPIYear,
  team_years: [],
};

export type EventsData = {
  year: APIYear;
  events: APIEvent[];
};

export const emptyEventData: EventsData = {
  year: emptyAPIYear,
  events: [],
};
