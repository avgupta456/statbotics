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
  search: "",
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
      <div className="h-40 m-2 p-4 rounded flex flex-col border-[1px] shadow hover:bg-blue-100 cursor-pointer">
        <div className="w-full flex-grow text-lg font-bold mb-4">{truncate(event.name, 45)}</div>
        <div className="w-full mb-2">
          {location} - Week {event.week}
        </div>
        {event.status === "Ongoing" && <div className="w-full">{event.status_str}</div>}
      </div>
    </Link>
  );
};

const Summary = ({ data }: { data: EventData }) => {
  // Currently always set to true --> No offseason events shown
  const [filterOffseason, setFilterOffseason] = useState(true);
  const [filters, setFilters] = useState(defaultFilters);
  const [expanded, setExpanded] = useState("");

  const search = filters?.["search"] || "";

  const cutoffN = 4;

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
        return (
          <div key={`${name}_section`} className="w-full">
            <div className="w-full flex mt-4 mb-4 items-center">
              <div className="text-xl md:text-2xl font-bold">{`${name} Events (${count})`}</div>
              {count > cutoffN && (
                <button
                  className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
                  onClick={() =>
                    setExpanded(expanded === name.toLowerCase() ? "" : name.toLowerCase())
                  }
                >
                  {expanded === name.toLowerCase() ? "Show Less" : "Show More"}
                </button>
              )}
            </div>
            <div className="w-full flex flex-wrap justify-center items-center mb-4">
              {events.map((event) => (
                <div key={event.key} className="w-full md:w-1/2 lg:w-1/4">
                  <EventCard event={event} />
                </div>
              ))}
            </div>
          </div>
        );
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

export default Summary;
