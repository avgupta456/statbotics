"use client";

import React, { FC, useState } from "react";

import { FilterBar, filterData } from "../../../components/filter";
import { APIEvent } from "../../../components/types/api";
import { EventData } from "../types";

const defaultFilters = {
  week: "",
  country: "",
  state: "",
  district: "",
  search: "",
};

const EventsLayout = ({
  year,
  data,
  SectionComponent,
}: {
  year: number;
  data: EventData;
  SectionComponent: FC<{ name: string; year: number; data: EventData }>;
}) => {
  // Currently always set to true --> No offseason events shown
  const [filterOffseason, setFilterOffseason] = useState(true);
  const [filters, setFilters] = useState(defaultFilters);

  const search = filters?.["search"] || "";

  const filteredData: APIEvent[] | undefined = filterData(data, filters).filter(
    (event: APIEvent) =>
      (!filterOffseason || !event.offseason) &&
      (event.key?.toLowerCase().includes(search.toLowerCase()) ||
        event.name?.toLowerCase().includes(search.toLowerCase()))
  );

  const N = filteredData?.length;
  const ongoingN = filteredData?.filter((event) => event.status === "Ongoing").length;
  const ongoingEvents = filteredData
    ?.filter((event) => event.status === "Ongoing")
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1));

  const upcomingN = filteredData?.filter((event) => event.status === "Upcoming").length;
  const upcomingEvents = filteredData
    ?.filter((event) => event.status === "Upcoming")
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1));

  const completedN = filteredData?.filter((event) => event.status === "Completed").length;
  const completedEvents = filteredData
    ?.filter((event) => event.status === "Completed")
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1));

  return (
    <div className="w-full h-full flex flex-col items-center">
      <div className="flex justify-center mb-4">
        <FilterBar defaultFilters={defaultFilters} filters={filters} setFilters={setFilters} />
      </div>
      {[
        { count: ongoingN, events: ongoingEvents, name: "Ongoing" },
        { count: upcomingN, events: upcomingEvents, name: "Upcoming" },
        { count: completedN, events: completedEvents, name: "Completed" },
      ].map(({ count, events, name }) => {
        if (count === 0) {
          return null;
        }
        return <SectionComponent key={name} name={name} year={year} data={events} />;
      })}
      {N === 0 && (
        <div className="w-full h-full flex justify-center items-center">
          <div>No Events Found</div>
        </div>
      )}
      <div className="h-4" />
    </div>
  );
};

export default EventsLayout;
