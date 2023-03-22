"use client";

import React, { useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { validateFilters } from "../../../components/filter";
import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { EventData } from "../types";
import Tabs from "./tabs";

export const metadata = {
  title: "Events - Statbotics",
};

async function getEventData(year: number) {
  const cacheData = getWithExpiry(`events_${year}`);
  if (cacheData && cacheData?.events?.length > 10) {
    log("Used Local Storage: " + year);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/events/${year}`, { next: { revalidate: 60 } });
  log(`/events/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(`events_${year}`, data, expiry);
  return data;
}

// cache this page for 1 hour
export const revalidate = 60 * 60;

const Page = () => {
  const { eventDataDict, setEventDataDict, year, setYear } = useContext(AppContext);
  const data: EventData | undefined = eventDataDict[year];
  const [error, setError] = useState(false);

  const searchParams = useSearchParams();
  const paramFilters = validateFilters(
    {
      year: searchParams.get("year"),
      week: searchParams.get("week"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
      search: searchParams.get("search"),
    },
    ["year", "week", "country", "state", "district", "search"],
    [undefined, "", "", "", "", ""]
  );

  const [filters, setFilters] = useState({
    week: paramFilters.week,
    country: paramFilters.country,
    state: paramFilters.state,
    district: paramFilters.district,
    search: paramFilters.search,
  });

  useEffect(() => {
    const filterYear = parseInt(paramFilters.year || year);
    if (filterYear !== year) setYear(filterYear);
  }, [paramFilters.year, year, setYear]);

  useEffect(() => {
    setError(false);
  }, [year]);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (eventDataDict[year] || error) {
        return;
      }

      const data: EventData = await getEventData(year);

      if (!data) {
        setError(true);
      } else {
        setEventDataDict((prev) => ({ ...prev, [year]: data }));
      }
    };

    getDataForYear(year);
  }, [eventDataDict, setEventDataDict, year, error]);

  return (
    <PageLayout title="Events" year={year} setYear={setYear}>
      <Tabs data={data} error={error} filters={filters} setFilters={setFilters} />
    </PageLayout>
  );
};

export default Page;
