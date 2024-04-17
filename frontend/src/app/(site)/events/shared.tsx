"use client";

import React, { FC } from "react";

import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { CURR_WEEK, CURR_YEAR } from "../../../constants";
import { APIEvent } from "../../../types/api";
import { EventsData } from "../../../types/data";

const defaultFilters = {
  week: "",
  country: "",
  state: "",
  district: "",
  offseason: "",
  search: "",
};

const EventsLayout = ({
  data,
  filters,
  setFilters,
  SectionComponent,
}: {
  data: EventsData;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
  SectionComponent: FC<{ name: string; data: EventsData }>;
}) => {
  if (data?.year?.year === CURR_YEAR) {
    defaultFilters["offseason"] = "season";
  }

  const actualFilters = Object.keys(defaultFilters).reduce(
    (acc, key) => ({ ...acc, [key]: filters[key] || defaultFilters[key] }),
    {}
  );

  const search = actualFilters?.["search"] || "";

  const filteredData: APIEvent[] | undefined = filterData(data.events, actualFilters).filter(
    (event: APIEvent) =>
      event.key?.toLowerCase().includes(search.toLowerCase()) ||
      event.name?.toLowerCase().includes(search.toLowerCase())
  );

  const sortedData: APIEvent[] | undefined = filteredData?.sort((a, b) =>
    a.start_date === b.start_date
      ? b.epa.mean > a.epa.mean
        ? 1
        : -1
      : a.start_date > b.start_date
      ? 1
      : -1
  );

  const N = filteredData?.length;

  // ex: 2024-01-01
  const today = new Date().toISOString().split("T")[0];

  const ongoingEvents = sortedData
    ?.filter((event) => event.status === "Ongoing" && event.week >= CURR_WEEK)
    .sort((a, b) => {
      if (a.current_match > 0 && b.current_match === 0) return -1;
      if (a.current_match === 0 && b.current_match > 0) return 1;
      return a.epa.mean > b.epa.mean ? -1 : 1;
    });
  const ongoingN = ongoingEvents.length;

  const upcomingEvents = sortedData?.filter((event) => event.status === "Upcoming");
  const upcomingN = upcomingEvents.length;

  const completedEvents = sortedData?.filter(
    (event) => event.status === "Completed" || (event.status == "Ongoing" && event.week < CURR_WEEK)
  );
  const completedN = completedEvents.length;

  return (
    <div className="w-full h-full flex flex-col items-center">
      <div className="flex justify-center mb-4">
        <FilterBar
          defaultFilters={defaultFilters}
          filters={actualFilters}
          setFilters={setFilters}
        />
      </div>
      {[
        { count: ongoingN, events: ongoingEvents, name: "Ongoing" },
        { count: upcomingN, events: upcomingEvents, name: "Upcoming" },
        { count: completedN, events: completedEvents, name: "Completed" },
      ].map(({ count, events, name }) => {
        if (count === 0) {
          return null;
        }
        return <SectionComponent key={name} name={name} data={{ year: data.year, events }} />;
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
