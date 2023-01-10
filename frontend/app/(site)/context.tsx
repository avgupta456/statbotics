import React, { createContext } from "react";

import { CURR_YEAR } from "../../constants";
import { EventData, TeamYearData } from "./types";

export const AppContext = createContext({
  teamYearDataDict: {},
  eventDataDict: {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearDataDict: { [key: number]: TeamYearData };
  eventDataDict: { [key: number]: EventData };
  year: number;
  setYear: (year: number) => void;
});
