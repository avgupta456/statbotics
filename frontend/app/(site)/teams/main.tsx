"use client";

import React, { useContext, useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { TeamYearData } from "../types";
import Tabs from "./tabs";

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

const PageContent = ({ paramFilters }: { paramFilters: { [key: string]: any } }) => {
  const {
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    year,
    setYear,
  } = useContext(AppContext);
  const data: TeamYearData | undefined = teamYearDataDict[year] || teamYearMiniDataDict[year];
  const [error, setError] = useState(false);

  const [filters, setFilters] = useState({
    country: paramFilters.country,
    state: paramFilters.state,
    district: paramFilters.district,
    is_competing: year === CURR_YEAR && "",
  });

  useEffect(() => {
    const filterYear = parseInt(paramFilters.year || year);
    if (filterYear !== year) setYear(filterYear);
  }, [paramFilters.year, year, setYear]);

  useEffect(() => {
    setError(false);
  }, [year]);

  useEffect(() => {
    const getMiniDataForYear = async (year: number) => {
      if (teamYearMiniDataDict[year] || error) {
        return;
      }

      const data: TeamYearData = await getTeamYearData(year, 50);

      if (!data) {
        setError(true);
      } else {
        setTeamYearMiniDataDict((prev) => ({ ...prev, [year]: data }));
      }
    };

    getMiniDataForYear(year);
  }, [teamYearMiniDataDict, setTeamYearMiniDataDict, year, error]);

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
      <Tabs year={year} data={data} error={error} filters={filters} setFilters={setFilters} />
    </PageLayout>
  );
};

export default PageContent;
