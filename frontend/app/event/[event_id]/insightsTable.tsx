import React from "react";

import EventInsightsTable, {
  TeamEventInsights,
} from "../../../components/Table/EventInsightsTable";
import { Data } from "./types";
import { round } from "../../../utils";
import { TableKey } from "../../../components/Table/shared";

const PageEventInsightsTable = ({ data }: { data: Data }) => {
  const eventInsightsData: TeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent.num,
        team: teamEvent.team,
        epa: round(teamEvent.epa, 1),
        auto_epa: round(teamEvent.auto_epa, 1),
        teleop_epa: round(teamEvent.teleop_epa, 1),
        endgame_epa: round(teamEvent.endgame_epa, 1),
        rp_1_epa: round(teamEvent.rp_1_epa, 2),
        rp_2_epa: round(teamEvent.rp_2_epa, 2),
        rank: teamEvent.rank,
      };
    })
    .sort((a, b) => a.rank - b.rank);

  const EventInsightsTableProps = {
    data: eventInsightsData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Event Insights</p>
      <EventInsightsTable {...EventInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageEventInsightsTable;
