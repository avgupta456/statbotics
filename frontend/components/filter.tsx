import React from "react";
import Select from "react-select";

import {
  canadaOptions,
  countryOptions,
  districtOptions,
  usaOptions,
  weekOptions,
  yearOptions,
} from "./filterConstants";

export const filterData = (data: any[] | undefined, filter: any) => {
  if (!data) {
    return [];
  }

  let filteredData = data;
  Object.keys(filter).forEach((key) => {
    const value = filter[key];
    if (value !== "") {
      filteredData = filteredData.filter((datum) => datum[key] === value);
    }
  });
  return filteredData;
};

export const FilterBar = ({
  defaultFilters,
  filters,
  setFilters,
}: {
  defaultFilters: { [key: string]: any };
  filters: { [key: string]: any };
  setFilters: any;
}) => {
  const filterKeys = Object.keys(filters);
  const stateOptions = filters?.country === "Canada" ? canadaOptions : usaOptions;
  const stateLabel = filters?.country === "Canada" ? "Province" : "State";

  const smartSetFilters = (key: string, value: any) => {
    // Can add more logic here if needed
    if (value === "") {
      return setFilters({ ...filters, [key]: "" });
    }
    if (key === "week") {
      return setFilters({ ...filters, [key]: value });
    } else if (key === "country") {
      return setFilters({ ...filters, country: value, state: "", district: "" });
    } else if (key === "state") {
      const country = usaOptions.map((x) => x.value).includes(value) ? "USA" : "Canada";
      return setFilters({ ...filters, country, state: value, district: "" });
    } else if (key === "district") {
      return setFilters({ ...filters, country: "", state: "", district: value });
    }
  };

  return (
    <div className="flex flex-row items-end justify-center">
      <button
        id="clear-filters"
        className="filter_button w-32"
        onClick={() => setFilters(defaultFilters)}
      >
        Clear Filters
      </button>
      {[
        { key: "year", label: "Year", options: yearOptions },
        { key: "week", label: "Week", options: weekOptions },
        { key: "country", label: "Country", options: countryOptions },
        { key: "state", label: stateLabel, options: stateOptions },
        { key: "district", label: "District", options: districtOptions },
      ].map((filter) => {
        if (filterKeys.includes(filter.key)) {
          const currValue = filters[filter.key];
          let currOptions: any[] = filter.options; // value is number | string
          let currLabel = currOptions.find((option) => option.value === currValue)?.label;
          let placeholder = currLabel === "All";
          if (placeholder) {
            currLabel = `${filter.label}`;
          }
          return (
            <div key={filter.key} className="flex flex-col items-center justify-center">
              <Select
                instanceId={"filter-select" + filter.key}
                className={"w-36 h-10 text-sm mr-2 text-gray-800"}
                styles={{
                  singleValue: (provided) => ({
                    ...provided,
                    color: placeholder ? "#a0aec0" : "#2d3748",
                  }),
                  menu: (provided) => ({ ...provided, zIndex: 9999 }),
                }}
                options={filter.options.map((option) => ({
                  value: option.value,
                  label: option.label,
                }))}
                onChange={(e) => smartSetFilters(filter.key, e?.value)}
                value={{ value: currValue, label: currLabel }}
              />
            </div>
          );
        }
      })}
    </div>
  );
};
