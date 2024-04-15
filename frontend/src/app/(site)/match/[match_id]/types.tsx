import {
  APIEvent,
  APIMatch,
  APITeamEvent,
  APITeamMatch,
  APIYear,
} from "../../../../components/types/api";

export type Data = {
  year: APIYear;
  event: APIEvent;
  team_events: APITeamEvent[];
  match: APIMatch;
  team_matches: APITeamMatch[];
};
