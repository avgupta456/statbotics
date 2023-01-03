"use client";

import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { DebounceInput } from "react-debounce-input";

import YearInsightsTable, { TeamYearInsights } from "../../../components/Table/YearInsightsTable";
import { TableKey } from "../../../components/Table/shared";
import { FilterBar, filterData } from "../../../components/filter";
import { round, truncate } from "../../../utils";
import { TeamYearData } from "../types";

const PageTeamInsightsTable = ({ year, data }: { year: number; data: TeamYearData }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [filters, setFilters] = useState({
    country: "",
    state: "",
    district: "",
  });
  const [search, setSearch] = useState("");

  const yearInsightsData: TeamYearInsights[] = filterData(data.team_years, filters)
    .filter(
      (teamYear) =>
        teamYear.team?.toLowerCase().includes(search.toLowerCase()) ||
        teamYear.num.toString().includes(search.toLowerCase())
    )
    .map((teamYear) => {
      return {
        num: teamYear.num ?? -1,
        team: teamYear.team ? truncate(teamYear.team, 30) : "N/A",
        epa_rank: teamYear.epa_rank ?? -1,
        norm_epa: round(teamYear.norm_epa, 0) ?? 0,
        epa: round(teamYear.total_epa, 1) ?? "N/A",
        auto_epa: round(teamYear.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamYear.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamYear.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamYear.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamYear.rp_2_epa, 2) ?? "N/A",
        record: `${teamYear.wins}-${teamYear.losses}-${teamYear.ties}` ?? "N/A",
      };
    })
    .sort((a, b) => b.norm_epa - a.norm_epa);

  const YearInsightsTableProps = {
    data: yearInsightsData,
    stats: data.year,
    year,
    disableHighlight,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="flex items-center justify-center mb-4">
        <button
          className="filter_button w-32"
          onClick={() => setDisableHighlight(!disableHighlight)}
        >
          {disableHighlight ? "Enable" : "Disable"} Color
        </button>
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <FilterBar filters={filters} setFilters={setFilters} />
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <DebounceInput
          minLength={2}
          debounceTimeout={300}
          className="w-40 p-2 relative rounded text-sm border-[1px] border-gray-200 focus:outline-inputBlue"
          placeholder="Search"
          onChange={(e) => setSearch(e.target.value)}
        />
        <CSVLink data={yearInsightsData} filename={`${year}_team_insights.csv`}>
          <button className="filter_button w-20 ml-2">Export</button>
        </CSVLink>
      </div>
      <YearInsightsTable {...YearInsightsTableProps} />
      <TableKey />
    </div>
  );
};

export default PageTeamInsightsTable;
