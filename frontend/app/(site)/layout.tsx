"use client";

import React, { useState } from "react";

import { CURR_YEAR } from "../../constants";
import { AppContext } from "./context";
import { EventData, MatchData, TeamYearData } from "./types";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [teamYearMiniDataDict, setTeamYearMiniDataDict] = useState<{ [key: number]: TeamYearData }>(
    {}
  );
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamYearData }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: EventData }>({});
  const [matchDataDict, setMatchDataDict] = useState<{ [key: number]: MatchData }>({});
  const [year, setYear] = useState(CURR_YEAR);

  return (
    <AppContext.Provider
      value={{
        teamYearMiniDataDict,
        setTeamYearMiniDataDict,
        teamYearDataDict,
        setTeamYearDataDict,
        eventDataDict,
        setEventDataDict,
        matchDataDict,
        setMatchDataDict,
        year,
        setYear,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}
