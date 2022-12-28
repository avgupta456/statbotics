import React, { createContext } from "react";

import { Data } from "./types";

export const AppContext = createContext({
  dataDict: {},
  year: 2022,
  setYear: (year: number) => {},
} as {
  dataDict: { [key: number]: Data };
  year: number;
  setYear: (year: number) => void;
});
