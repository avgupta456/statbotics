"use client";

import React, { useState } from "react";

import EventInsightsTable, {
  TeamEventInsights,
} from "../../../components/Table/EventInsightsTable";
import { TableKey } from "../../../components/Table/shared";
import { round } from "../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ data }: { data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const eventInsightsData: TeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent.num ?? -1,
        team: teamEvent.team ?? "N/A",
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
    stats: data.year_stats,
    disableHighlight,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="w-full text-2xl font-bold text-gray-800 mb-4">Team Insights</div>
      <div className="flex items-end justify-center mb-2">
        <button
          className="filter_button w-32"
          onClick={() => setDisableHighlight(!disableHighlight)}
        >
          {disableHighlight ? "Enable" : "Disable"} Color
        </button>
      </div>
      <EventInsightsTable {...EventInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageEventInsightsTable;
