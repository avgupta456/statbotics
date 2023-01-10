"use client";

import React, { useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../constants";
import { round } from "../../utils";
import { getWithExpiry, setWithExpiry } from "../localStorage";
import { AppContext } from "./context";
import { EventData, TeamYearData } from "./types";

async function getTeamYearData(year: number) {
  const cacheData = getWithExpiry(`team_years_${year}`);
  if (cacheData && cacheData?.team_years?.length > 100) {
    console.log("Used Local Storage: " + year);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team_years/` + year, { next: { revalidate: 60 } });
  console.log(`/team_years/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`team_years_${year}`, data, expiry);
  return data;
}

async function getEventData(year: number) {
  const cacheData = getWithExpiry(`events_${year}`);
  if (cacheData && cacheData?.events?.length > 10) {
    console.log("Used Local Storage: " + year);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/events/${year}`, { next: { revalidate: 60 } });
  console.log(`/events/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`events_${year}`, data, expiry);
  return data;
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamYearData }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: EventData }>({});
  const [year, setYear] = useState(CURR_YEAR);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (teamYearDataDict[year]) {
        return;
      }

      const data: TeamYearData = await getTeamYearData(year);
      setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getDataForYear(year);
  }, [teamYearDataDict, year]);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (eventDataDict[year]) {
        return;
      }

      const data: EventData = await getEventData(year);
      setEventDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getDataForYear(year);
  }, [eventDataDict, year]);

  return (
    <AppContext.Provider value={{ teamYearDataDict, eventDataDict, year, setYear }}>
      {children}
    </AppContext.Provider>
  );
}
