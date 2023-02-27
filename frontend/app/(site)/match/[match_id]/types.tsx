import { APIEvent, APIMatch, APITeamMatch, APIYear } from "../../../../components/types/api";

export type Data = {
  year: APIYear;
  event: APIEvent;
  team_events: APITeamMatch[];
  match: APIMatch;
  team_matches: APITeamMatch[];
};
