"use client";

import React, { useCallback, useContext, useEffect, useState } from "react";

import { useRouter } from "next/router";

import { getYearTeamYears } from "../../api/teams";
import { validateFilters } from "../../components/filter";
import { CURR_YEAR } from "../../constants";
import SiteLayout from "../../layouts/siteLayout";
import { AppContext } from "../../pagesContent/context";
import PageLayout from "../../pagesContent/shared/layout";
import Tabs from "../../pagesContent/teams/tabs";
import { TeamYearsData } from "../../types/data";

const InnerPage = () => {
  const [loadAllData, setLoadAllData] = useState(false);
  const { teamYearDataDict, setTeamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearsData | undefined = teamYearDataDict[year];
  const [error, setError] = useState(false);

  const router = useRouter();
  const { year: queryYear, country, state, district } = router.query;

  useEffect(() => {
    document.title = "Teams - Statbotics";
  }, []);

  const getFilters = useCallback(() => {
    const filters = {
      year: queryYear,
      country,
      state,
      district,
      is_competing: year === CURR_YEAR ? "" : undefined,
    };

    return validateFilters(
      filters,
      ["year", "country", "state", "district"],
      [undefined, "", "", ""]
    );
  }, [queryYear, country, state, district, year]);

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
      if (error) {
        return;
      }

      const numTeamYears = teamYearDataDict[year]?.team_years?.length ?? 0;

      let data: TeamYearsData | null = null;
      if (numTeamYears < 100 && !loadAllData) {
        data = await getYearTeamYears(year, 100);
      } else if (numTeamYears < 101 && loadAllData) {
        data = await getYearTeamYears(year);
      } else {
        return;
      }

      if (!data) {
        setError(true);
      } else {
        setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
      }
    };

    getDataForYear(year);
  }, [teamYearDataDict, setTeamYearDataDict, year, error, loadAllData]);

  return (
    <PageLayout title="Teams" year={year} setYear={setYear}>
      <Tabs
        year={year}
        data={data}
        error={error}
        filters={filters}
        setFilters={setFilters}
        loadAllData={loadAllData}
        setLoadAllData={setLoadAllData}
      />
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
