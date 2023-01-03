"use client";

import React, { useState } from "react";
import { DebounceInput } from "react-debounce-input";

import Link from "next/link";

import { FilterBar, filterData } from "../../../components/filter";
import { APIEvent } from "../../../components/types/api";
import { truncate } from "../../../utils";
import { EventData } from "../types";

const defaultFilters = {
  week: "",
  country: "",
  state: "",
  district: "",
};

const EventCard = ({ event }: { event: APIEvent }) => {
  let location = event.country;
  if (event.state) {
    location = `${event.state}, ${location}`;
  }
  if (event.district) {
    location = `${location} (${event.district.toUpperCase()})`;
  }
  return (
    <Link href={`/event/${event.key}`}>
      <div className="h-32 m-2 p-4 rounded border-[1px] shadow hover:bg-blue-100 cursor-pointer">
        <div className="w-full text-xl font-bold mb-4">{truncate(event.name, 35)}</div>
        {location} - Week {event.week}
      </div>
    </Link>
  );
};

const Summary = ({ data }: { data: EventData }) => {
  // Currently always set to true --> No offseason events shown
  const [filterOffseason, setFilterOffseason] = useState(true);
  const [filters, setFilters] = useState(defaultFilters);
  const [search, setSearch] = useState("");
  const [expanded, setExpanded] = useState("");

  const cutoffN = 8;

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
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1))
    .slice(0, expanded === "ongoing" ? undefined : cutoffN);

  const upcomingN = filteredData?.filter((event) => event.status === "Upcoming").length;
  const upcomingEvents = filteredData
    ?.filter((event) => event.status === "Upcoming")
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1))
    .slice(0, expanded === "upcoming" ? undefined : cutoffN);

  const completedN = filteredData?.filter((event) => event.status === "Completed").length;
  const completedEvents = filteredData
    ?.filter((event) => event.status === "Completed")
    .sort((a, b) => (a.end_date > b.end_date ? 1 : -1))
    .slice(0, expanded === "completed" ? undefined : cutoffN);

  return (
    <div className="w-full h-full flex flex-col items-center">
      <div className="flex items-end justify-center mb-4">
        <FilterBar defaultFilters={defaultFilters} filters={filters} setFilters={setFilters} />
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <DebounceInput
          minLength={2}
          debounceTimeout={300}
          className="w-40 p-2 relative rounded text-sm border-[1px] border-gray-200 focus:outline-inputBlue"
          placeholder="Search"
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      {ongoingN > 0 && (
        <>
          <div className="w-full flex mt-4 mb-4 items-center">
            <div className="text-2xl font-bold">{`Ongoing Events (${ongoingN})`}</div>
            {ongoingN > cutoffN && (
              <button
                className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
                onClick={() => setExpanded(expanded === "ongoing" ? "" : "ongoing")}
              >
                {expanded === "ongoing" ? "Show Less" : "Show More"}
              </button>
            )}
          </div>
          <div className="w-full flex flex-wrap justify-center items-center">
            {ongoingEvents.map((event) => (
              <div key={event.key} className="w-1/4">
                <EventCard event={event} />
              </div>
            ))}
          </div>
          <div className="w-full h-1 bg-gray-200 my-8" />
        </>
      )}
      {upcomingN > 0 && (
        <>
          <div className="w-full flex mt-4 mb-4 items-center">
            <div className="text-2xl font-bold">{`Upcoming Events (${upcomingN})`}</div>
            {upcomingN > cutoffN && (
              <button
                className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
                onClick={() => setExpanded(expanded === "upcoming" ? "" : "upcoming")}
              >
                {expanded === "upcoming" ? "Show Less" : "Show More"}
              </button>
            )}
          </div>
          <div className="w-full flex flex-wrap justify-center items-center">
            {upcomingEvents.map((event) => (
              <div key={event.key} className="w-1/4">
                <EventCard event={event} />
              </div>
            ))}
          </div>
          <div className="w-full h-1 bg-gray-200 my-8" />
        </>
      )}
      {completedN > 0 && (
        <>
          <div className="w-full flex mt-4 mb-4 items-center">
            <div className="text-2xl font-bold">{`Completed Events (${completedN})`}</div>
            {completedN > cutoffN && (
              <button
                className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
                onClick={() => setExpanded(expanded === "completed" ? "" : "completed")}
              >
                {expanded === "completed" ? "Show Less" : "Show More"}
              </button>
            )}
          </div>
          <div className="w-full flex flex-wrap justify-center items-center">
            {completedEvents.map((event) => (
              <div key={event.key} className="w-1/4">
                <EventCard event={event} />
              </div>
            ))}
          </div>
        </>
      )}
      {N === 0 && (
        <div className="w-full h-full flex justify-center items-center">
          <div>No Events Found</div>
        </div>
      )}
      <div className="h-4" />
    </div>
  );
};

export default Summary;
