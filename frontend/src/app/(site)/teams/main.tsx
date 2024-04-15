"use client";

import React, { useContext, useEffect, useState } from "react";

import { getYearTeamYears } from "../../../api/teams";
import { CURR_YEAR } from "../../../constants";
import { APITeamYear, APIYear } from "../../../types/api";
import { TeamYearData } from "../../../types/data";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import Tabs from "./tabs";

const PageContent = ({ paramFilters }: { paramFilters: { [key: string]: any } }) => {
  const { teamYearDataDict, setTeamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearData | undefined = teamYearDataDict[year];
  const [error, setError] = useState(false);

  const [filters, setFilters] = useState({
    country: paramFilters.country,
    state: paramFilters.state,
    district: paramFilters.district,
    is_competing: year === CURR_YEAR && "",
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
      if (teamYearDataDict[year] || error) {
        return;
      }

      const data: TeamYearData = await getYearTeamYears(year);

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

export default PageContent;
