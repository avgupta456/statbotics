/* eslint-disable no-unused-vars */

/* eslint-disable @typescript-eslint/no-unused-vars */
import { createContext, useContext } from "react";

import { EventData, TeamYearData, YearData } from "../types";
import { CURR_YEAR } from "../utils/constants";

export const DataContext = createContext({
  teamYearMiniDataDict: {},
  setTeamYearMiniDataDict: (teamYearMiniDataDict: { [key: number]: TeamYearData }) => {},
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: TeamYearData }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: EventData }) => {},
  yearDataDict: {},
  setyearDataDict: (yearDataDict: { [key: number]: YearData }) => {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearMiniDataDict: { [key: number]: TeamYearData };
  setTeamYearMiniDataDict: any;
  teamYearDataDict: { [key: number]: TeamYearData };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: EventData };
  setEventDataDict: any;
  yearDataDict: { [key: number]: YearData };
  setyearDataDict: any;
  year: number;
  setYear: (year: number) => void;
});

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error("useData must be used within a DataProvider");
  }
  return context;
};
