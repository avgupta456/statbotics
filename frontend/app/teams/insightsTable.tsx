"use client";

import React, { useState } from "react";

import YearInsightsTable, { TeamYearInsights } from "../../components/Table/YearInsightsTable";
import { TableKey } from "../../components/Table/shared";
import { FilterBar, filterData } from "../../components/filter";
import { round, truncate } from "../../utils";
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
        team: teamYear.team ? truncate(teamYear.team, 30) : "N/A",
        epa_rank: teamYear.epa_rank ?? -1,
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
      <div className="flex items-end justify-center mb-2">
        <button
          className="filter_button w-32"
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
