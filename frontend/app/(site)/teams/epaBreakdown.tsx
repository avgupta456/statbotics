"use client";

import React, { useState } from "react";

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
  const [showProjections, setShowProjections] = useState(true);

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
          includeProjections={year === CURR_YEAR}
          showProjections={showProjections}
          setShowProjections={setShowProjections}
        />
      </div>
      <EPABreakdownTable
        year={year}
        yearData={data.year}
        data={filterData(data.team_years, actualFilters)}
      />
    </div>
  );
};

export default EPABreakdownSection;
