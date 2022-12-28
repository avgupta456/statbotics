import React, { createContext } from "react";

import { Data } from "./types";

export const AppContext = createContext({
  dataDict: {},
  getDataForYear: (year: number) => {},
} as { dataDict: { [key: number]: Data }; getDataForYear: (year: number) => void });
