"use client";

import React, { useContext, useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { EventData, MatchData } from "../types";
import Tabs from "./tabs";

async function getMatchData(year: number) {
  const cacheData = getWithExpiry(`matches_${year}`);
  if (cacheData) {
    log("Used Local Storage: " + year);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/matches/${year}`, { next: { revalidate: 60 } });
  log(`/matches/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`matches_${year}`, data, expiry);
  return data;
}

// cache this page for 1 minute
export const revalidate = 60;

const Page = () => {
  const { matchDataDict, setMatchDataDict, year, setYear } = useContext(AppContext);
  const data: MatchData | undefined = matchDataDict[year];
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
  }, [year]);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (matchDataDict[year] || error) {
        return;
      }

      const data: MatchData = await getMatchData(year);

      if (!data) {
        setError(true);
      } else {
        setMatchDataDict((prev) => ({ ...prev, [year]: data }));
      }
    };

    getDataForYear(year);
  }, [matchDataDict, setMatchDataDict, year, error]);

  return (
    <PageLayout title="Matches" year={year} setYear={setYear}>
      <Tabs year={year} data={data} error={error} />
    </PageLayout>
  );
};

export default Page;
