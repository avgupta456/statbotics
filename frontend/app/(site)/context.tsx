import React, { createContext } from "react";

import { TeamYearData } from "./types";

export const AppContext = createContext({
  dataDict: {},
  year: 2022,
  setYear: (year: number) => {},
} as {
  dataDict: { [key: number]: TeamYearData };
  year: number;
  setYear: (year: number) => void;
});
