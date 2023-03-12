import React, { createContext } from "react";

import { CURR_YEAR } from "../../constants";
import { EventData, MatchData, TeamYearData } from "./types";

export const AppContext = createContext({
  teamYearMiniDataDict: {},
  setTeamYearMiniDataDict: (teamYearMiniDataDict: { [key: number]: TeamYearData }) => {},
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: TeamYearData }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: EventData }) => {},
  matchDataDict: {},
  setMatchDataDict: (matchDataDict: { [key: number]: MatchData }) => {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearMiniDataDict: { [key: number]: TeamYearData };
  setTeamYearMiniDataDict: any;
  teamYearDataDict: { [key: number]: TeamYearData };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: EventData };
  setEventDataDict: any;
  matchDataDict: { [key: number]: MatchData };
  setMatchDataDict: any;
  year: number;
  setYear: (year: number) => void;
});
