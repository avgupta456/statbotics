"use client";

import React, { useState } from "react";

import { BACKEND_URL } from "../../constants";
import { AppContext } from "./context";
import { getWithExpiry, setWithExpiry } from "./local_storage";
import { Data } from "./types";

async function getData(year: number) {
  const cacheData = getWithExpiry(`team_years_${year}`);
  if (cacheData && cacheData?.team_years?.length > 100) {
    console.log("Using cached team data for year: " + year);
    return cacheData;
  }

  const res = await fetch(`${BACKEND_URL}/team_years/` + year);
  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  setWithExpiry(`team_years_${year}`, data, 60); // 60 seconds
  return data;
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const [dataDict, setDataDict] = useState<{ [key: number]: Data }>({});

  const getDataForYear = async (year: number) => {
    if (dataDict[year]) {
      return;
    }

    console.log("Fetching team data for year: " + year);
    const start = performance.now();
    const data: Data = await getData(year);
    console.log(
      "Fetched team data for year: " +
        year +
        ". Took " +
        Math.round(performance.now() - start) +
        "ms"
    );
    setDataDict((prev) => ({ ...prev, [year]: data }));
  };

  return <AppContext.Provider value={{ dataDict, getDataForYear }}>{children}</AppContext.Provider>;
}
