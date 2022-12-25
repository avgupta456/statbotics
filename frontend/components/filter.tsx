import React from "react";
import Select from "react-select";

import {
  canadaOptions,
  countryOptions,
  districtOptions,
  usaOptions,
  yearOptions,
} from "./filterConstants";

export const filterData = (data: any, filter: any) => {
  let filteredData = data;
  Object.keys(filter).forEach((key) => {
    const value = filter[key];
    if (value) {
      filteredData = filteredData.filter((datum) => datum[key] === value);
    }
  });
  return filteredData;
};

export const FilterBar = ({ filters, setFilters }: { filters: any; setFilters: any }) => {
  const filterKeys = Object.keys(filters);
  const stateOptions = filters?.country === "Canada" ? canadaOptions : usaOptions;

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
    <div className="flex flex-row items-end justify-center">
      <button
        id="clear-filters"
        className="border-2 border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer h-10 w-32 px-2 mr-2 rounded text-sm flex items-center justify-center"
        onClick={() => setFilters({ country: "", state: "", district: "" })}
      >
        Clear Filters
      </button>
      {[
        { key: "year", options: yearOptions },
        { key: "country", options: countryOptions },
        { key: "state", options: stateOptions },
        { key: "district", options: districtOptions },
      ].map((filter) => {
        if (filterKeys.includes(filter.key)) {
          return (
            <div key={filter.key} className="flex flex-col items-center justify-center">
              <p className="w-full pl-1 text-sm text-gray-500 capitalize">
                {filter.key === "state" && filters?.country === "Canada" ? "province" : filter.key}
              </p>
              <Select
                className="w-36 h-10 text-sm mr-2"
                styles={{
                  menu: (provided) => ({ ...provided, zIndex: 9999 }),
                }}
                options={filter.options.map((option) => ({
                  value: option.value,
                  label: option.label,
                }))}
                onChange={(e) => smartSetFilters(filter.key, e?.value)}
                value={{
                  value: filters[filter.key],
                  label: filter.options.find((option) => option.value === filters[filter.key])
                    ?.label,
                }}
              />
            </div>
          );
        }
      })}
    </div>
  );
};
