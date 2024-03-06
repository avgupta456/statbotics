"use client";

import React, { useState } from "react";

import Link from "next/link";

import { APIEvent } from "../../../components/types/api";
import { formatEventName } from "../../../utils";
import { EventData } from "../types";
import EventsLayout from "./shared";

const EventCard = ({ event }: { event: APIEvent }) => {
  let location = event.country;
  if (event.state) {
    location = `${event.state}, ${location}`;
  }
  if (event.district) {
    location = `${location} (${event.district.toUpperCase()})`;
  }

  const formatDates = (start: Date, end: Date) => {
    const startMonth = start.toUTCString().split(" ")[2];
    const endMonth = end.toUTCString().split(" ")[2];
    const startDate = start.getUTCDate();
    const endDate = end.getUTCDate();
    if (startMonth === endMonth && startDate === endDate) {
      return `${startMonth} ${startDate}`;
    }
    return `${startMonth} ${startDate} to ${endMonth} ${endDate}`;
  };

  return (
    <Link href={`/event/${event.key}`}>
      <div className="h-40 m-2 p-4 rounded flex flex-col border-[1px] shadow hover:bg-blue-100 cursor-pointer">
        <div className="w-full flex-grow text-lg font-bold mb-4">
          {formatEventName(event.name, 45)}
        </div>
        <div className="w-full mb-2">
          Week {event.week}, {formatDates(new Date(event.start_date), new Date(event.end_date))}
        </div>
        {event.status === "Ongoing" && <div className="w-full">{event.status_str}</div>}
      </div>
    </Link>
  );
};

const Summary = ({
  data,
  filters,
  setFilters,
}: {
  data: EventData;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const [expanded, setExpanded] = useState("");
  const cutoffN = 8;

  return (
    <EventsLayout
      data={data}
      filters={filters}
      setFilters={setFilters}
      SectionComponent={({ name, data }) => {
        const count = data?.events?.length || 0;
        const showEvents = data?.events?.slice(0, expanded === name ? undefined : cutoffN) || [];

        return (
          <div className="w-full">
            <div className="w-full flex mt-4 mb-4 items-center">
              <div className="text-xl md:text-2xl font-bold">{`${name} Events (${count})`}</div>
              {count > cutoffN && (
                <button
                  className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
                  onClick={() => setExpanded(expanded === name ? "" : name)}
                >
                  {expanded === name ? "Show Less" : "Show More"}
                </button>
              )}
            </div>
            <div className="w-full flex flex-wrap justify-center items-center mb-4">
              {showEvents.map((event) => (
                <div key={event.key} className="w-full md:w-1/2 lg:w-1/4">
                  <EventCard event={event} />
                </div>
              ))}
            </div>
          </div>
        );
      }}
    />
  );
};

export default Summary;
