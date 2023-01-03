"use client";

import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { DebounceInput } from "react-debounce-input";

import EventInsightsTable, {
  TeamEventInsights,
} from "../../../../components/Table/EventInsightsTable";
import { TableKey } from "../../../../components/Table/shared";
import { round, truncate } from "../../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ eventId, data }: { eventId: string; data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [search, setSearch] = useState("");

  const eventInsightsData: TeamEventInsights[] = data.team_events
    .filter(
      (teamEvent) =>
        teamEvent.team?.toLowerCase().includes(search.toLowerCase()) ||
        teamEvent.num.toString().includes(search.toLowerCase())
    )
    .map((teamEvent) => {
      return {
        num: teamEvent.num ?? -1,
        team: teamEvent.team ? truncate(teamEvent.team, 30) : "N/A",
        epa: round(teamEvent.total_epa, 1) ?? "N/A",
        auto_epa: round(teamEvent.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamEvent.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamEvent.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamEvent.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamEvent.rp_2_epa, 2) ?? "N/A",
        rank: teamEvent.rank ?? -1,
      };
    })
    .sort((a, b) => a.rank - b.rank);

  const EventInsightsTableProps = {
    data: eventInsightsData,
    stats: data.year,
    disableHighlight,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="flex items-end justify-center mb-4">
        <button
          className="filter_button w-32"
          onClick={() => setDisableHighlight(!disableHighlight)}
        >
          {disableHighlight ? "Enable" : "Disable"} Color
        </button>
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <DebounceInput
          minLength={2}
          debounceTimeout={300}
          className="w-40 p-2 relative rounded text-sm border-[1px] border-gray-200 focus:outline-inputBlue"
          placeholder="Search"
          onChange={(e) => setSearch(e.target.value)}
        />
        <CSVLink data={eventInsightsData} filename={`${eventId}_team_insights.csv`}>
          <button className="filter_button w-20 ml-2">Export</button>
        </CSVLink>
      </div>
      <EventInsightsTable {...EventInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageEventInsightsTable;
