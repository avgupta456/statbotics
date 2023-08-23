"use client";

import React, { useContext, useEffect, useState } from "react";

import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import Tabs from "./tabs";

const PageContent = ({ paramFilters }: { paramFilters: { [key: string]: any } }) => {
  const { year, setYear } = useContext(AppContext);
  const [error, setError] = useState(false);

  const [filters, setFilters] = useState({
    week: paramFilters.week,
    country: paramFilters.country,
    state: paramFilters.state,
    district: paramFilters.district,
    elim: "",
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

export default PageContent;
