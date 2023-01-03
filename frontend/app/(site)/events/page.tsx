"use client";

import React, { useContext, useState } from "react";
import { DebounceInput } from "react-debounce-input";
import Select from "react-select";

import { FilterBar, filterData } from "../../../components/filter";
import { yearOptions } from "../../../components/filterConstants";
import { APIEvent } from "../../../components/types/api";
import { AppContext } from "../context";
// store types in (site) root so layout can access them
import { EventData } from "../types";

const Page = () => {
  const { eventDataDict, year, setYear } = useContext(AppContext);
  const data: EventData | undefined = eventDataDict[year];

  const [filters, setFilters] = useState({
    country: "",
    state: "",
    district: "",
  });
  const [search, setSearch] = useState("");

  const filteredData: APIEvent[] | undefined = filterData(data, filters).filter(
    (event: APIEvent) =>
      event.key?.toLowerCase().includes(search.toLowerCase()) ||
      event.name?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="w-full h-full flex-grow flex flex-col p-4">
      <div className="h-full container mx-auto flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <Select
            instanceId={"year-select"}
            className="w-28"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={yearOptions}
            onChange={(e) => setYear((e?.value ?? 2023) as number)}
            value={{
              value: year.toString(),
              label: year.toString(),
            }}
          />
          <p className="text-2xl lg:text-3xl ml-4">Event Lookup</p>
        </div>
        <div className="w-full flex flex-col justify-center items-center">
          <div className="flex items-end justify-center mb-4">
            <FilterBar filters={filters} setFilters={setFilters} />
            <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
            <DebounceInput
              minLength={2}
              debounceTimeout={300}
              className="w-40 p-2 relative rounded text-sm border-[1px] border-gray-200 focus:outline-inputBlue"
              placeholder="Search"
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        {filteredData.length}
      </div>
    </div>
  );
};

export default Page;
