"use client";

import React, { useContext, useEffect, useState } from "react";

import { getYearEvents } from "../../../server/events";
import { EventsData } from "../../../types/data";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import Tabs from "./tabs";

const PageContent = ({ paramFilters }: { paramFilters: { [key: string]: any } }) => {
  const { eventDataDict, setEventDataDict, year, setYear } = useContext(AppContext);
  const data: EventsData | undefined = eventDataDict[year];
  const [error, setError] = useState(false);

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

export default PageContent;
