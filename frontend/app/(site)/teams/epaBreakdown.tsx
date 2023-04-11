"use client";

import React, { useEffect, useState } from "react";

import EPABreakdownTable from "../../../components/Table/EPABreakdownTable";
import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { CURR_YEAR } from "../../../constants";
import { getEPABreakdown, getEPABreakdownPercentiles } from "../../../utils";
import { TeamYearData } from "../types";

const EPABreakdownSection = ({
  year,
  data,
  filters,
  setFilters,
}: {
  year: number;
  data: TeamYearData;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  let defaultFilters = {
    country: "",
    state: "",
    district: "",
  };

  if (year === CURR_YEAR) {
    defaultFilters["is_competing"] = "";
  }

  const actualFilters = Object.keys(defaultFilters).reduce(
    (acc, key) => ({ ...acc, [key]: filters[key] || defaultFilters[key] }),
    {}
  );

  const [epaBreakdownPercentiles, setEPABreakdownPercentiles] = useState(null);
  const [epaBreakdown, setEPABreakdown] = useState(null);

  useEffect(() => {
    if (!epaBreakdownPercentiles && data.year) {
      getEPABreakdownPercentiles(setEPABreakdownPercentiles);
    }

    if (!epaBreakdown && data.year) {
      getEPABreakdown(setEPABreakdown);
    }
  }, [epaBreakdownPercentiles, epaBreakdown, data.year]);

  const epaBreakdownData = data.team_years.map((teamYear) => {
    const teamYearEPABreakdown = epaBreakdown?.[teamYear.num] ?? {};
    return { ...teamYear, epa_breakdown: teamYearEPABreakdown };
  });

  const epaBreakdownYearData = { ...data.year, epa_breakdown_stats: epaBreakdownPercentiles ?? {} };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="flex items-center justify-center">
        <FilterBar
          defaultFilters={defaultFilters}
          filters={actualFilters}
          setFilters={setFilters}
          includeProjections={false}
        />
      </div>
      {epaBreakdownPercentiles && epaBreakdown ? (
        <EPABreakdownTable
          year={year}
          yearData={epaBreakdownYearData}
          data={filterData(epaBreakdownData, actualFilters)}
          csvFilename={`${year}_epa_breakdown.csv`}
        />
      ) : (
        <div className="w-full flex-grow flex flex-col items-center justify-center">
          <div className="text-gray-700 mt-4">Loading data, please wait...</div>
        </div>
      )}
    </div>
  );
};

export default EPABreakdownSection;
