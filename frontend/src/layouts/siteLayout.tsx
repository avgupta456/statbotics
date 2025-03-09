"use client";

import React, { useState } from "react";

import { CURR_YEAR } from "../constants";
import { AppContext } from "../pagesContent/context";
import { EventsData, TeamYearsData } from "../types/data";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamYearsData }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: EventsData }>({});
  const [year, setYear] = useState(CURR_YEAR);

  return (
    <AppContext.Provider
      value={{
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
