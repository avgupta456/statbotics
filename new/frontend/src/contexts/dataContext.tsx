/* eslint-disable no-unused-vars */

/* eslint-disable @typescript-eslint/no-unused-vars */
import { createContext, useContext } from "react";

import { APIEvent, APIShortEvent, APIShortTeam, APITeamYear, APIYear } from "../types/api";
import { CURR_YEAR } from "../utils/constants";

export const DataContext = createContext({
  allTeams: [],
  setAllTeams: (allTeams: APIShortTeam[]) => {},
  allEvents: [],
  setAllEvents: (allEvents: APIShortEvent[]) => {},
  teamYearDataDict: {},
  setTeamYearDataDict: (teamYearDataDict: { [key: number]: APITeamYear[] }) => {},
  eventDataDict: {},
  setEventDataDict: (eventDataDict: { [key: number]: APIEvent[] }) => {},
  yearDataDict: {},
  setYearDataDict: (yearDataDict: { [key: number]: APIYear }) => {},
} as {
  allTeams: APIShortTeam[];
  setAllTeams: any;
  allEvents: APIShortEvent[];
  setAllEvents: any;
  teamYearDataDict: { [key: number]: APITeamYear[] };
  setTeamYearDataDict: any;
  eventDataDict: { [key: number]: APIEvent[] };
  setEventDataDict: any;
  yearDataDict: { [key: number]: APIYear };
  setYearDataDict: any;
});

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error("useData must be used within a DataProvider");
  }
  return context;
};
