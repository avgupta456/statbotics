import React, { createContext } from "react";

import { CURR_YEAR } from "../../constants";
import { EventData, TeamYearData } from "./types";

export const AppContext = createContext({
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: TeamYearData }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: EventData }) => {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearDataDict: { [key: number]: TeamYearData };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: EventData };
  setEventDataDict: any;
  year: number;
  setYear: (year: number) => void;
});
