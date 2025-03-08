"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { validateFilters } from "../../../components/filter";
import { getYearEvents } from "../../../server/events";
import { EventsData } from "../../../types/data";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import Tabs from "./tabs";

const Page = () => {
  const { eventDataDict, setEventDataDict, year, setYear } = useContext(AppContext);
  const data: EventsData | undefined = eventDataDict[year];
  const [error, setError] = useState(false);

  const searchParams = useSearchParams();

  useEffect(() => {
    document.title = "Events - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: searchParams.get("year"),
      week: searchParams.get("week"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
      search: searchParams.get("search"),
    };

    return validateFilters(
      filters,
      ["year", "week", "country", "state", "district", "search"],
      [undefined, "", "", "", "", ""]
    );
  }, [searchParams]);

  const [filters, setFilters] = useState(getFilters);

  useEffect(() => {
    const filterYear = parseInt(searchParams.get("year") || year.toString());
    if (filterYear !== year) setYear(filterYear);

    setFilters(getFilters());
  }, [searchParams, year, setYear, getFilters]);

  useEffect(() => {
    setError(false);
  }, [year]);

  useEffect(() => {
    const getDataForYear = async (year: number) => {
      if (eventDataDict[year] || error) {
        return;
      }

      const data: EventsData = await getYearEvents(year);

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
