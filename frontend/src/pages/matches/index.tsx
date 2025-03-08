"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { validateFilters } from "../../components/filter";
import { AppContext } from "../../pagesContent/context";
import Tabs from "../../pagesContent/matches/tabs";
import PageLayout from "../../pagesContent/shared/layout";

const Page = () => {
  const { year, setYear } = useContext(AppContext);
  const [error, setError] = useState(false);

  const searchParams = useSearchParams();

  useEffect(() => {
    document.title = "Matches - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: searchParams.get("year"),
      week: searchParams.get("week"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
      playoff: "",
      filterMatches: 15,
      sortMatches: "max_epa",
      refresh: 0,
    };

    return validateFilters(
      filters,
      ["year", "week", "country", "state", "district"],
      [undefined, "", "", "", ""]
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

  return (
    <PageLayout title="Matches" year={year} setYear={setYear}>
      <Tabs year={year} error={error} filters={filters} setFilters={setFilters} />
    </PageLayout>
  );
};

export default Page;
