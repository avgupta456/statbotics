"use client";

import React, { useContext, useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { TeamYearData } from "../types";
import Tabs from "./tabs";

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

const Page = () => {
  const { teamYearDataDict, setTeamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearData | undefined = teamYearDataDict[year];
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
  }, [year]);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (teamYearDataDict[year] || error) {
        return;
      }

      const data: TeamYearData = await getTeamYearData(year);

      if (!data) {
        setError(true);
      } else {
        setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
      }
    };

    getDataForYear(year);
  }, [teamYearDataDict, setTeamYearDataDict, year, error]);

  return (
    <PageLayout title="Teams" year={year} setYear={setYear}>
      <Tabs year={year} data={data} error={error} />
    </PageLayout>
  );
};

export default Page;
