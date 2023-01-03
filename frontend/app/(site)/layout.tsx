"use client";

import React, { useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../constants";
import { round } from "../../utils";
import { getWithExpiry, setWithExpiry } from "../localStorage";
import { AppContext } from "./context";
import { TeamYearData } from "./types";

async function getTeamYearData(year: number) {
  const cacheData = getWithExpiry(`team_years_${year}`);
  if (cacheData && cacheData?.team_years?.length > 100) {
    console.log("Used Local Storage: " + year);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team_years/` + year);
  console.log(`/team_years/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`team_years_${year}`, data, expiry);
  return data;
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const [dataDict, setDataDict] = useState<{ [key: number]: TeamYearData }>({});
  const [year, setYear] = useState(2022);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (dataDict[year]) {
        return;
      }

      const data: TeamYearData = await getTeamYearData(year);
      setDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getDataForYear(year);
  }, [dataDict, year]);

  return <AppContext.Provider value={{ dataDict, year, setYear }}>{children}</AppContext.Provider>;
}
