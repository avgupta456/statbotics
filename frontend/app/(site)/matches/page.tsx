"use client";

import React, { useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { validateFilters } from "../../../components/filter";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import Tabs from "./tabs";

// cache this page for 1 minute
export const revalidate = 60;

const Page = () => {
  const { year, setYear } = useContext(AppContext);
  const [error, setError] = useState(false);

  const searchParams = useSearchParams();
  const paramFilters = validateFilters(
    {
      year: searchParams.get("year"),
      week: searchParams.get("week"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
    },
    ["year", "week", "country", "state", "district"],
    [undefined, "", "", "", "", ""]
  );

  const [filters, setFilters] = useState({
    week: paramFilters.week,
    country: paramFilters.country,
    state: paramFilters.state,
    district: paramFilters.district,
    playoff: "",
    filterMatches: "",
    sortMatches: "predicted_time",
    refresh: 0,
  });

  useEffect(() => {
    const filterYear = parseInt(paramFilters.year || year);
    if (filterYear !== year) setYear(filterYear);
  }, [paramFilters.year, year, setYear]);

  useEffect(() => {
    setError(false);
  }, [year]);

  return (
    <PageLayout title="Matches" year={year} setYear={setYear}>
      <Tabs year={year} error={error} filters={filters} setFilters={setFilters} />
    </PageLayout>
  );
};

export default Page;
