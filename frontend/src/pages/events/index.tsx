"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useRouter } from "next/router";

import { getYearEvents } from "../../api/events";
import { validateFilters } from "../../components/filter";
import SiteLayout from "../../layouts/siteLayout";
import { AppContext } from "../../pagesContent/context";
import Tabs from "../../pagesContent/events/tabs";
import PageLayout from "../../pagesContent/shared/layout";
import { EventsData } from "../../types/data";

const InnerPage = () => {
  const { eventDataDict, setEventDataDict, year, setYear } = useContext(AppContext);
  const data: EventsData | undefined = eventDataDict[year];
  const [error, setError] = useState(false);

  const router = useRouter();
  const { year: queryYear, week, country, state, district, search } = router.query;

  useEffect(() => {
    document.title = "Events - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: queryYear,
      week,
      country,
      state,
      district,
      search,
    };

    return validateFilters(
      filters,
      ["year", "week", "country", "state", "district", "search"],
      [undefined, "", "", "", "", ""]
    );
  }, [queryYear, week, country, state, district, search]);

  const [filters, setFilters] = useState(getFilters);

  useEffect(() => {
    if (queryYear) {
      const filterYear = parseInt(queryYear as string);
      if (filterYear !== year) setYear(filterYear);
    }

    setFilters(getFilters());
  }, [queryYear, year, setYear, getFilters]);

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

const Page = () => {
  return (
    <SiteLayout>
      <InnerPage />
    </SiteLayout>
  );
};

export default Page;
