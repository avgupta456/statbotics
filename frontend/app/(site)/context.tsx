import React, { createContext } from "react";

import { EventData, TeamYearData } from "./types";

export const AppContext = createContext({
  teamYearDataDict: {},
  eventDataDict: {},
  year: 2022,
  setYear: (year: number) => {},
} as {
  teamYearDataDict: { [key: number]: TeamYearData };
  eventDataDict: { [key: number]: EventData };
  year: number;
  setYear: (year: number) => void;
});
