"use client";

import React, { useContext, useEffect, useMemo, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import TabsSection from "../shared/tabs";
import { TeamYearData } from "../types";
import Event from "./event";
import Match from "./match";

async function getTeamYearData(year: number, limit?: number | null) {
  let url_suffix = `/team_years/` + year;
  let storage_key = `team_years_${year}`;
  if (limit) {
    url_suffix += `?limit=${limit}&metric=epa_end`;
    storage_key += `_${limit}`;
  }

  const cacheData = getWithExpiry(storage_key);
  if (cacheData && cacheData?.team_years?.length > 0) {
    log("Used Local Storage: " + storage_key);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}${url_suffix}`, { next: { revalidate: 60 } });
  log(`${url_suffix} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(storage_key, data, expiry);
  return data;
}

const Tabs = () => {
  const { teamYearDataDict, setTeamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearData | undefined = teamYearDataDict[year];
  const [error, setError] = useState(false);

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

  const MemoizedMatch = useMemo(() => <Match data={data} />, [data]);
  const MemoizedEvent = useMemo(() => <Event data={data} year={year} />, [data, year]);

  const tabs = [
    { title: "Match", content: MemoizedMatch },
    { title: "Event", content: MemoizedEvent },
  ];

  return (
    <PageLayout title="Hypothetical" year={year} setYear={setYear}>
      <TabsSection loading={data === undefined} error={error} tabs={tabs} />
    </PageLayout>
  );
};

export default Tabs;
