"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useSearchParams } from "next/navigation";

import { getYearTeamYears } from "../../api/teams";
import { validateFilters } from "../../components/filter";
import { CURR_YEAR } from "../../constants";
import { AppContext } from "../../pagesContent/context";
import PageLayout from "../../pagesContent/shared/layout";
import Tabs from "../../pagesContent/teams/tabs";
import { TeamYearsData } from "../../types/data";

const Page = () => {
  const { teamYearDataDict, setTeamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearsData | undefined = teamYearDataDict[year];
  const [error, setError] = useState(false);

  const searchParams = useSearchParams();

  useEffect(() => {
    document.title = "Teams - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: searchParams.get("year"),
      country: searchParams.get("country"),
      state: searchParams.get("state"),
      district: searchParams.get("district"),
      is_competing: year === CURR_YEAR ? "" : undefined,
    };

    return validateFilters(
      filters,
      ["year", "country", "state", "district"],
      [undefined, "", "", ""]
    );
  }, [searchParams, year]);

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
      if (teamYearDataDict[year] || error) {
        return;
      }

      const data: TeamYearsData = await getYearTeamYears(year);

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

export default Page;
