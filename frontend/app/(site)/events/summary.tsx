"use client";

import React, { useState } from "react";
import { DebounceInput } from "react-debounce-input";

import { FilterBar, filterData } from "../../../components/filter";
import { APIEvent } from "../../../components/types/api";
import { EventData } from "../types";

const Summary = ({ data }: { data: EventData }) => {
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
      {filteredData.length}
    </div>
  );
};

export default Summary;
