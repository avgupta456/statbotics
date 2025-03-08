import React, { createContext } from "react";

import { CURR_YEAR } from "../constants";
import { EventsData, TeamYearsData } from "../types/data";

export const AppContext = createContext({
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: TeamYearsData }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: EventsData }) => {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearDataDict: { [key: number]: TeamYearsData };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: EventsData };
  setEventDataDict: any;
  year: number;
  setYear: (year: number) => void;
});
