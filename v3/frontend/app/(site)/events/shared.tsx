"use client";

import React, { FC, useState } from "react";

import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { APIEvent } from "../../../components/types/api";
import { CURR_WEEK, CURR_YEAR } from "../../../constants";
import { EventData } from "../types";

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
  data: EventData;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
  SectionComponent: FC<{ name: string; data: EventData }>;
}) => {
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

  const N = filteredData?.length;

  const ongoingEvents = filteredData
    ?.filter(
      (event) => event.status === "Ongoing" && (event.year !== CURR_YEAR || event.week >= CURR_WEEK)
    )
    .sort((a, b) => (b.epa_mean > a.epa_mean ? 1 : -1));
  const ongoingN = ongoingEvents.length;

  const upcomingEvents = filteredData
    ?.filter(
      (event) =>
        event.status === "Upcoming" && (event.year !== CURR_YEAR || event.week >= CURR_WEEK)
    )
    .sort((a, b) => (a.week === b.week ? (b.epa_mean > a.epa_mean ? 1 : -1) : a.week - b.week));
  const upcomingN = upcomingEvents.length;

  const completedEvents = filteredData
    ?.filter(
      (event) =>
        event.status === "Completed" && (event.year !== CURR_YEAR || event.week <= CURR_WEEK)
    )
    .sort((a, b) => (a.week === b.week ? (b.epa_mean > a.epa_mean ? 1 : -1) : a.week - b.week));
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
