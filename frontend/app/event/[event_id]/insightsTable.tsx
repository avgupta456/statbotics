import React from "react";

import EventInsightsTable, {
  TeamEventInsights,
} from "../../../components/Table/EventInsightsTable";
import { TableFooter, TableKey } from "../../../components/Table/shared";
import { round } from "../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ data }: { data: Data }) => {
  const eventInsightsData: TeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent.num ?? -1,
        team: teamEvent.team ?? "N/A",
        epa: round(teamEvent.epa, 1) ?? "N/A",
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
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Event Insights</p>
      <TableKey />
      <EventInsightsTable {...EventInsightsTableProps} />
      <TableFooter />
    </div>
  );
};

export default PageEventInsightsTable;
