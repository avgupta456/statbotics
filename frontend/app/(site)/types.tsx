import { APITeamYear, APIYear, emptyAPIYear } from "../../components/types/api";

export type TeamYearData = {
  team_years: APITeamYear[];
  year: APIYear;
};

export const emptyTeamYearData: TeamYearData = {
  team_years: [],
  year: emptyAPIYear,
};
