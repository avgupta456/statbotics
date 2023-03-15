"use client";

import React, { FC, useState } from "react";

import { FilterBar, filterData } from "../../../components/filter";
import { APIEvent } from "../../../components/types/api";
import { CURR_WEEK, CURR_YEAR } from "../../../constants";
import { EventData } from "../types";

const defaultFilters = {
  week: "",
  country: "",
  state: "",
  district: "",
  search: "",
};

const EventsLayout = ({
  data,
  SectionComponent,
}: {
  data: EventData;
  SectionComponent: FC<{ name: string; data: EventData }>;
}) => {
  // Currently always set to true --> No offseason events shown
  const [filterOffseason, setFilterOffseason] = useState(true);
  const [filters, setFilters] = useState(defaultFilters);

  const search = filters?.["search"] || "";

  const filteredData: APIEvent[] | undefined = filterData(data.events, filters).filter(
    (event: APIEvent) =>
      (!filterOffseason || !event.offseason) &&
      (event.key?.toLowerCase().includes(search.toLowerCase()) ||
        event.name?.toLowerCase().includes(search.toLowerCase()))
  );

  const N = filteredData?.length;

  const ongoingEvents = filteredData
    ?.filter(
      (event) =>
        event.status === "Ongoing" && (event.year !== CURR_YEAR || event.week === CURR_WEEK)
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
