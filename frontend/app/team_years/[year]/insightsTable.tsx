"use client";

import React, { useState } from "react";

import YearInsightsTable, { TeamYearInsights } from "../../../components/Table/YearInsightsTable";
import { TableKey } from "../../../components/Table/shared";
import { FilterBar, filterData } from "../../../components/filter";
import { round } from "../../../utils";
import { Data } from "./types";

const PageEventInsightsTable = ({ data }: { data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [filters, setFilters] = useState({
    country: "",
    state: "",
    district: "",
  });

  const yearInsightsData: TeamYearInsights[] = filterData(data.team_years, filters)
    .map((teamYear) => {
      return {
        num: teamYear.num ?? -1,
        team: teamYear.name ?? "N/A",
        epa: round(teamYear.total_epa, 1) ?? 0,
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
    disableHighlight,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Team Insights</p>
      <div className="flex items-end justify-center mb-2">
        <button
          className="border-2 border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer h-10 w-32 px-2 mr-2 rounded text-sm flex items-center justify-center"
          onClick={() => setDisableHighlight(!disableHighlight)}
        >
          {disableHighlight ? "Enable" : "Disable"} Color
        </button>
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <FilterBar filters={filters} setFilters={setFilters} />
      </div>
      <YearInsightsTable {...YearInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageEventInsightsTable;
