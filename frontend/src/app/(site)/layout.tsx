"use client";

import React, { useState } from "react";

import { CURR_YEAR } from "../../constants";
import { AppContext } from "./context";
import { EventData, TeamYearData } from "./types";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [teamYearMiniDataDict, setTeamYearMiniDataDict] = useState<{ [key: number]: TeamYearData }>(
    {}
  );
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamYearData }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: EventData }>({});
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
        year,
        setYear,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}
