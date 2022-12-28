"use client";

import React, { useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../constants";
import { AppContext } from "./context";
import { getWithExpiry, setWithExpiry } from "./localStorage";
import { Data } from "./types";

async function getData(year: number) {
  const cacheData = getWithExpiry(`team_years_${year}`);
  if (cacheData && cacheData?.team_years?.length > 100) {
    console.log("Using cached data for year: " + year);
    return cacheData;
  }

  const res = await fetch(`${BACKEND_URL}/team_years/` + year);
  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`team_years_${year}`, data, expiry);
  return data;
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const [dataDict, setDataDict] = useState<{ [key: number]: Data }>({});
  const [year, setYear] = useState(2022);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (dataDict[year]) {
        return;
      }

      console.log("Fetching year: " + year);
      const start = performance.now();
      const data: Data = await getData(year);
      const end = performance.now();
      console.log("Fetched year: " + year + ". Took " + Math.round(end - start) + "ms");
      setDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getDataForYear(year);
  }, [dataDict, year]);

  return <AppContext.Provider value={{ dataDict, year, setYear }}>{children}</AppContext.Provider>;
}
