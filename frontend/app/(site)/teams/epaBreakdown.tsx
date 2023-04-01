"use client";

import React from "react";

import EPABreakdownTable from "../../../components/Table/EPABreakdownTable";
import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { CURR_YEAR } from "../../../constants";
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
      <EPABreakdownTable
        year={year}
        yearData={data.year}
        data={filterData(data.team_years, actualFilters)}
        csvFilename={`${year}_epa_breakdown.csv`}
      />
    </div>
  );
};

export default EPABreakdownSection;
