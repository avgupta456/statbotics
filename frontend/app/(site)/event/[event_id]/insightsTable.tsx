"use client";

import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { DebounceInput } from "react-debounce-input";
import { MdClose, MdCloudDownload, MdColorLens, MdSearch } from "react-icons/md";

import EventInsightsTable, {
  TeamEventInsights,
} from "../../../../components/Table/EventInsightsTable";
import { TableKey } from "../../../../components/Table/shared";
import { round, truncate } from "../../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ eventId, data }: { eventId: string; data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
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
        total_epa: round(teamEvent.total_epa, 1) ?? "N/A",
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
      <div className="w-full px-4 flex items-center justify-center">
        <div className="flex-grow">
          {showSearch ? (
            <div className="flex">
              <DebounceInput
                minLength={2}
                debounceTimeout={300}
                className="max-w-60 p-2 relative rounded text-sm border-[2px] border-inputBlue focus:outline-none"
                placeholder="Search"
                onChange={(e) => setSearch(e.target.value)}
              />
              <MdClose
                className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
                onClick={() => setShowSearch(!showSearch)}
              />
            </div>
          ) : (
            <div className="text-lg text-gray-800">Event Insights</div>
          )}
        </div>
        <div className="tooltip" data-tip="Search">
          <MdSearch
            className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
            onClick={() => setShowSearch(!showSearch)}
          />
        </div>
        <div className="tooltip" data-tip={disableHighlight ? "Enable Color" : "Disable Color"}>
          <MdColorLens
            className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
            onClick={() => setDisableHighlight(!disableHighlight)}
          />
        </div>
        <div className="tooltip" data-tip="Download CSV">
          <CSVLink data={eventInsightsData} filename={`${eventId}_team_insights.csv`}>
            <MdCloudDownload className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer" />
          </CSVLink>
        </div>
      </div>
      <EventInsightsTable {...EventInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageEventInsightsTable;
