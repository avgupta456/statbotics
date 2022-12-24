import React from "react";

import YearInsightsTable, { TeamYearInsights } from "../../../components/Table/YearInsightsTable";
import { TableFooter, TableKey } from "../../../components/Table/shared";
import { round } from "../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ data }: { data: Data }) => {
  const yearInsightsData: TeamYearInsights[] = data.team_years
    .map((teamYear) => {
      return {
        num: teamYear.num ?? -1,
        team: teamYear.name ?? "N/A",
        epa: round(teamYear.total_epa, 1) ?? "N/A",
        auto_epa: round(teamYear.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamYear.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamYear.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamYear.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamYear.rp_2_epa, 2) ?? "N/A",
        record: `${teamYear.wins}-${teamYear.losses}-${teamYear.ties}` ?? "N/A",
      };
    })
    .sort((a, b) => b.epa - a.epa);

  const YearInsightsTableProps = {
    data: yearInsightsData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Team Insights</p>
      <TableKey />
      <YearInsightsTable {...YearInsightsTableProps} />
    </div>
  );
};

export default PageEventInsightsTable;
