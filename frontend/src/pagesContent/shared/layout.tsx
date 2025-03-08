"use client";

import React from "react";
import Select from "react-select";

import { yearOptions } from "../../components/filterConstants";
import { CURR_YEAR } from "../../constants";

const PageLayout = ({
  title,
  year,
  setYear,
  years,
  includeSummary,
  children,
}: {
  title: string;
  year?: number;
  setYear?: (year: number) => void;
  years?: number[];
  includeSummary?: boolean;
  children: React.ReactNode;
}) => {
  const finalYears = years ? years : yearOptions.map((option) => parseInt(option.value));
  let filteredYearOptions = yearOptions.filter((option) =>
    finalYears.includes(parseInt(option.value))
  );

  if (includeSummary) {
    filteredYearOptions = [{ value: "-1", label: "Summary" }, ...filteredYearOptions];
  }

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="w-full h-full flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          {year && setYear && (
            <Select
              instanceId="year-select"
              className="w-28"
              styles={{
                menu: (provided) => ({ ...provided, zIndex: 9999 }),
              }}
              options={filteredYearOptions}
              onChange={(e) => setYear((parseInt(e?.value) ?? CURR_YEAR) as number)}
              value={{
                value: year.toString(),
                label: year === -1 ? "Summary" : year.toString(),
              }}
            />
          )}
          <p className="text-2xl lg:text-3xl ml-3">{title}</p>
        </div>
        {children}
      </div>
    </div>
  );
};

export default PageLayout;
