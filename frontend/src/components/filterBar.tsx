"use client";

import React from "react";
import { DebounceInput } from "react-debounce-input";
import { BiShow } from "react-icons/bi";
import { MdRefresh } from "react-icons/md";
import Select from "react-select";

import {
  canadaOptions,
  competingOptions,
  countryOptions,
  districtOptions,
  filterMatchesOptions,
  playoffOptions,
  sortMatchesOptions,
  usaOptions,
  weekOptions,
  yearOptions,
} from "./filterConstants";

export const FilterBar = ({
  defaultFilters,
  filters,
  setFilters,
  includeProjections = false,
  showProjections = false,
  setShowProjections = () => {},
}: {
  defaultFilters: { [key: string]: any };
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
  includeProjections?: boolean;
  showProjections?: boolean;
  setShowProjections?: any;
}) => {
  const filterKeys = Object.keys(filters);
  const stateOptions = filters?.country === "Canada" ? canadaOptions : usaOptions;
  const stateLabel = filters?.country === "Canada" ? "Province" : "State";

  const smartSetFilters = (key: string, value: any) => {
    // Can add more logic here if needed
    if (key === "refresh") {
      return setFilters({ ...filters, refresh: filters.refresh + 1 });
    }

    if (value === "") {
      if (key === "country") return setFilters({ ...filters, country: "", state: "" });
      return setFilters({ ...filters, [key]: "" });
    }

    if (
      [
        "year",
        "week",
        "is_competing",
        "search",
        "playoff",
        "filterMatches",
        "sortMatches",
      ].includes(key)
    ) {
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
    <div className="flex flex-row flex-wrap items-end justify-center">
      <div className="tooltip mb-4" data-tip="Clear filters">
        <BiShow className="hover_icon" onClick={() => setFilters(defaultFilters)} />
      </div>
      {[
        { key: "year", label: "Year", options: yearOptions },
        { key: "week", label: "Week", options: weekOptions },
        { key: "country", label: "Country", options: countryOptions },
        { key: "state", label: stateLabel, options: stateOptions },
        { key: "district", label: "District", options: districtOptions },
        { key: "is_competing", label: "Competing", options: competingOptions },
        { key: "vbar", label: "", options: [] },
        { key: "playoff", label: "Comp Level", options: playoffOptions },
        { key: "filterMatches", label: "Time Range", options: filterMatchesOptions },
        { key: "sortMatches", label: "Sort Matches", options: sortMatchesOptions },
      ].map((filter) => {
        if (filter.key === "vbar" && filterKeys.includes("vbar")) {
          return <div key={filter.key} className="w-0.5 h-10 ml-2 mb-4 bg-gray-500 rounded" />;
        } else if (filterKeys.includes(filter.key)) {
          const currValue = filters[filter.key];
          let currOptions: any[] = filter.options; // value is number | string
          let currLabel = currOptions.find((option) => option.value === currValue)?.label;
          let placeholder = currValue === "";
          if (placeholder) {
            currLabel = `${filter.label}`;
          }
          return (
            <Select
              key={filter.key}
              instanceId={"filter-select" + filter.key}
              className={"text-xs w-24 ml-1 md:text-sm md:w-36 md:ml-2 mb-4 text-gray-800"}
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
          );
        }
      })}
      {filterKeys.includes("search") && (
        <>
          <div className="w-0.5 h-10 ml-2 mr-2 mb-4 bg-gray-500 rounded" />
          <DebounceInput
            minLength={2}
            debounceTimeout={300}
            className="w-40 p-2 mb-4 relative rounded text-sm border-[1px] border-gray-200 focus:outline-inputBlue"
            placeholder="Search"
            onChange={(e) => smartSetFilters("search", e.target.value)}
          />
        </>
      )}
      {includeProjections && (
        <>
          <div className="w-0.5 h-10 ml-2 mr-2 mb-4 bg-gray-500 rounded" />
          <div
            className="h-10 p-2 mb-4 rounded bg-gray-100 flex items-center justify-center cursor-pointer hover:bg-gray-200"
            onClick={() => setShowProjections(!showProjections)}
          >
            {`${showProjections ? "Hide" : "Show"} Projections`}
          </div>
        </>
      )}
      {filterKeys.includes("refresh") && (
        <div className="tooltip mb-4 ml-1 md:ml-2" data-tip="Refresh">
          <MdRefresh className="hover_icon" onClick={(e) => smartSetFilters("refresh", e)} />
        </div>
      )}
    </div>
  );
};
