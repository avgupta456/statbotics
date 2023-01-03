import { APIEvent, APIMatch, APITeamMatch, APIYear } from "../../../../components/types/api";

export type Data = {
  match: APIMatch;
  event: APIEvent;
  year: APIYear;
  team_matches: APITeamMatch[];
};
