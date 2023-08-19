import {
  APIEvent,
  APIMatch,
  APITeamEvent,
  APITeamMatch,
  APIYear,
} from "../../../../components/types/api";

export type Data = {
  event: APIEvent;
  matches: APIMatch[];
  team_events: APITeamEvent[];
  team_matches: APITeamMatch[];
  year: APIYear;
};
