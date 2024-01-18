/* eslint-disable no-unused-vars */

/* eslint-disable @typescript-eslint/no-unused-vars */
import { createContext, useContext } from "react";

import { EventData } from "../types";
import { APITeamYear, APIYear } from "../types/api";
import { CURR_YEAR } from "../utils/constants";

export const DataContext = createContext({
  teamYearMiniDataDict: {},
  setTeamYearMiniDataDict: (teamYearMiniDataDict: { [key: number]: APITeamYear[] }) => {},
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: APITeamYear[] }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: EventData }) => {},
  yearDataDict: {},
  setYearDataDict: (yearDataDict: { [key: number]: APIYear }) => {},
  year: CURR_YEAR,
  setYear: (year: number) => {},
} as {
  teamYearMiniDataDict: { [key: number]: APITeamYear[] };
  setTeamYearMiniDataDict: any;
  teamYearDataDict: { [key: number]: APITeamYear[] };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: EventData };
  setEventDataDict: any;
  yearDataDict: { [key: number]: APIYear };
  setYearDataDict: any;
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
