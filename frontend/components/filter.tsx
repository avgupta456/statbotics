import React from "react";

import {
  canadaOptions,
  countryOptions,
  districtOptions,
  usaOptions,
  yearOptions,
} from "./filterConstants";

type Datum = { [key: string]: any };
type Filter = { [key: string]: any };

export const filterData = (data: Datum[], filter: Filter) => {
  let filteredData = data;
  Object.keys(filter).forEach((key) => {
    const value = filter[key];
    if (value) {
      filteredData = filteredData.filter((datum) => datum[key] === value);
    }
  });
  return filteredData;
};

export const FilterBar = ({ filters, setFilters }: { filters: Filter; setFilters: any }) => {
  const filterKeys = Object.keys(filters);
  const stateOptions = filters.country === "Canada" ? canadaOptions : usaOptions;

  const smartSetFilters = (key: string, value: any) => {
    // Can add more logic here if needed
    if (value === "") {
      return setFilters({ ...filters, [key]: "" });
    }

    if (key === "country") {
      return setFilters({ country: value, state: "", district: "" });
    } else if (key === "state") {
      const country = usaOptions.map((x) => x.value).includes(value) ? "USA" : "Canada";
      setFilters({ country, state: value, district: "" });
    } else if (key === "district") {
      return setFilters({ country: "", state: "", district: value });
    }
  };

  return (
    <div className="flex flex-row items-center justify-center">
      {filterKeys.includes("year") && (
        <select
          className="border-2 border-gray-300 bg-white h-10 pl-5 pr-10 rounded-lg text-base focus:outline-none appearance-none"
          onChange={(e) => smartSetFilters("year", e.target.value)}
          value={filters.year}
        >
          {yearOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}
      {filterKeys.includes("country") && (
        <select
          className="border-2 border-gray-300 bg-white h-10 pl-5 pr-10 rounded-lg text-base focus:outline-none appearance-none"
          onChange={(e) => smartSetFilters("country", e.target.value)}
          value={filters.country}
        >
          {countryOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}
      {filterKeys.includes("state") && (
        <select
          className="border-2 border-gray-300 bg-white h-10 pl-5 pr-10 rounded-lg text-base focus:outline-none appearance-none"
          onChange={(e) => smartSetFilters("state", e.target.value)}
          value={filters.state}
        >
          {stateOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}
      {filterKeys.includes("district") && (
        <select
          className="border-2 border-gray-300 bg-white h-10 pl-5 pr-10 rounded-lg text-base focus:outline-none appearance-none"
          onChange={(e) => smartSetFilters("district", e.target.value)}
          value={filters.district}
        >
          {districtOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};
