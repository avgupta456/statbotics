"use client";

import React, { useMemo } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { APIEvent } from "../../../components/types/api";
import { EventData } from "../types";
import EventsLayout from "./shared";

export type EventInsights = {
  key: string;
  name: string;
};

const columnHelper = createColumnHelper<EventInsights>();

const EventTable = ({ year, events }: { year: number; events: APIEvent[] }) => {
  const eventInsightsData: EventInsights[] = events.map((event) => {
    return {
      key: event.key,
      name: event.name,
    };
  });
  // TODO: sort

  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("name", {
          cell: (info) => info.getValue(),
          header: "Name",
        }),
      ].filter(Boolean),
    []
  );

  return (
    <InsightsTable
      data={eventInsightsData}
      columns={columns}
      leftCol="name"
      rightCol="name"
      searchCols={["name"]}
      csvFilename={`${year}_event_insights.csv`}
    />
  );
};

const EventInsightsTable = ({ year, data }: { year: number; data: EventData }) => {
  return (
    <EventsLayout
      year={year}
      data={data}
      SectionComponent={({ name, year, data: events }) => {
        const count = events.length;
        return (
          <div key={`${name}_section`} className="w-full">
            <div className="w-full flex mt-4 mb-4 items-center text-xl md:text-2xl font-bold">
              {`${name} Events (${count})`}
            </div>
            <div className="w-full flex flex-wrap justify-center items-center mb-4">
              <EventTable year={year} events={events} />
            </div>
          </div>
        );
      }}
    />
  );
};

export default EventInsightsTable;
