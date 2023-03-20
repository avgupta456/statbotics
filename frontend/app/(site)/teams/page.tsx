"use client";

import React, { useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { validateFilters } from "../../../components/filter";
import {
  canadaOptions,
  countryOptions,
  districtOptions,
  usaOptions,
  yearOptions,
} from "../../../components/filterConstants";
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

// cache this page for 5 minutes
export const revalidate = 60 * 5;

const Page = () => {
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

  const searchParams = useSearchParams();
  const filters = validateFilters(
    {
      year: searchParams.get("year"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
    },
    ["year", "country", "state", "district"],
    [undefined, "", "", ""]
  );

  useEffect(() => {
    if (filters.year && filters.year !== year) {
      setYear(filters.year);
    }
  }, [filters.year, year, setYear]);

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
      <Tabs year={year} data={data} error={error} filters={filters} />
    </PageLayout>
  );
};

export default Page;
