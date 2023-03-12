"use client";

import React, { useMemo, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Link from "next/link";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { EventLink, formatCell, formatPercentileCell } from "../../../components/Table/shared";
import { round } from "../../../utils";
import { EventData } from "../types";
import EventsLayout from "./shared";

export type EventInsights = {
  event_key: string;
  name: string;
  week: number;
  date: string;
  country: string;
  district: string;
  state: string;
  status_str: string;
  matches: number;
  epa_acc: string;
  epa_mse: string;
  epa_max: number;
  epa_top8: number;
  epa_top24: number;
  epa_mean: number;
  video: string;
};

const columnHelper = createColumnHelper<EventInsights>();

const EventTable = ({ name, data }: { name: string; data: EventData }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const eventInsightsData: EventInsights[] = data.events
    .map((event) => {
      const startDate = event.start_date.slice(5).replace("-", "/").replace(/^0+/, "");
      const endDate = event.end_date.slice(5).replace("-", "/").replace(/^0+/, "");
      return {
        event_key: event.key,
        name: event.name,
        week: event.week,
        date: `${startDate} - ${endDate}`,
        country: event.country || "",
        district: event.district?.toUpperCase() || "",
        state: event.state || "",
        status_str: event.status_str || "",
        matches: Math.max(event.qual_matches, event.current_match) || 0,
        epa_acc: (100 * event.epa_acc)?.toFixed(1) + "%" || "N/A",
        epa_mse: event.epa_mse?.toFixed(3) || "N/A",
        epa_max: round(event.epa_max, 1) || 0,
        epa_top8: round(event.epa_top8, 1) || 0,
        epa_top24: round(event.epa_top24, 1) || 0,
        epa_mean: round(event.epa_mean, 1) || 0,
        video: `https://www.thebluealliance.com/gameday/${event.key}` || "",
      };
    })
    .sort((a, b) => b.epa_mean - a.epa_mean);

  const columns = useMemo<any>(
    () =>
      [
        name === "Ongoing" &&
          columnHelper.accessor("video", {
            cell: (info) => (
              <div className="w-16 md:w-20 mx-auto h-full flex justify-center items-center">
                <Link
                  href={info.getValue()}
                  rel="noopener noreferrer"
                  target="_blank"
                  className="text-sm"
                  style={{ color: "#9146FD" }}
                >
                  <BsTwitch size={20} />
                </Link>
              </div>
            ),
            header: "Video",
          }),
        columnHelper.accessor("name", {
          cell: (info) => EventLink({ key: info.row.original.event_key, event: info.getValue() }),
          header: "Name",
        }),
        columnHelper.accessor("week", {
          cell: (info) => formatCell(info),
          header: "Week",
        }),
        columnHelper.accessor("date", {
          cell: (info) => (
            <div className="w-24 mx-auto h-full flex justify-center items-center">
              {info.getValue()}
            </div>
          ),
          header: "Date",
        }),
        columnHelper.accessor("country", {
          cell: (info) => formatCell(info),
          header: "Country",
        }),
        columnHelper.accessor("district", {
          cell: (info) => formatCell(info),
          header: "District",
        }),
        columnHelper.accessor("state", {
          cell: (info) => formatCell(info),
          header: "State",
        }),
        name === "Ongoing" &&
          columnHelper.accessor("status_str", {
            cell: (info) => formatCell(info),
            header: "Status",
          }),
        name !== "Upcoming" &&
          columnHelper.accessor("matches", {
            cell: (info) => formatCell(info),
            header: "Matches",
          }),
        name === "Completed" &&
          columnHelper.accessor("epa_acc", {
            cell: (info) => formatCell(info),
            header: "Accuracy",
          }),
        name === "Completed" &&
          columnHelper.accessor("epa_mse", {
            cell: (info) => formatCell(info),
            header: "MSE",
          }),
        columnHelper.accessor("epa_max", {
          cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
          header: "Max EPA",
        }),
        columnHelper.accessor("epa_top8", {
          cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
          header: "Top 8 EPA",
        }),
        columnHelper.accessor("epa_top24", {
          cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
          header: "Top 24 EPA",
        }),
        columnHelper.accessor("epa_mean", {
          cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
          header: "Mean EPA",
        }),
      ].filter(Boolean),
    [data, name, disableHighlight]
  );

  return (
    <InsightsTable
      title={"Event Insights"}
      data={eventInsightsData}
      columns={columns}
      searchCols={["name"]}
      csvFilename={`${data.year.year}_event_insights.csv`}
      toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      includeKey={false}
    />
  );
};

const EventInsightsTable = ({ data }: { data: EventData }) => {
  return (
    <EventsLayout
      data={data}
      SectionComponent={({ name, data }) => {
        const count = data.events.length;
        return (
          <div key={`${name}_section`} className="w-full">
            <div className="w-full flex mt-4 mb-4 items-center text-xl md:text-2xl font-bold">
              {`${name} Events (${count})`}
            </div>
            <div className="w-full flex flex-wrap justify-center items-center mb-4">
              <EventTable name={name} data={data} />
            </div>
          </div>
        );
      }}
    />
  );
};

export default EventInsightsTable;
