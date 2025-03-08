"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useRouter } from "next/router";

import { validateFilters } from "../../components/filter";
import SiteLayout from "../../layouts/siteLayout";
import { AppContext } from "../../pagesContent/context";
import Tabs from "../../pagesContent/matches/tabs";
import PageLayout from "../../pagesContent/shared/layout";

const InnerPage = () => {
  const { year, setYear } = useContext(AppContext);
  const [error, setError] = useState(false);

  const router = useRouter();
  const { year: queryYear, week, country, state, district } = router.query;

  useEffect(() => {
    document.title = "Matches - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: queryYear,
      week,
      country,
      state,
      district,
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
  }, [queryYear, week, country, state, district]);

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

  return (
    <PageLayout title="Matches" year={year} setYear={setYear}>
      <Tabs year={year} error={error} filters={filters} setFilters={setFilters} />
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
