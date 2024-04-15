import { APITeamYear, APIYear, emptyAPIYear } from "./api";

export type TeamYearData = {
  year: APIYear;
  team_years: APITeamYear[];
};

export const emptyTeamYearData: TeamYearData = {
  year: emptyAPIYear,
  team_years: [],
};
