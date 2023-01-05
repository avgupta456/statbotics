"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatPercentileCell } from "../../../components/Table/shared";
import { FilterBar, filterData } from "../../../components/filter";
import { APITeamYear } from "../../../components/types/api";
import { formatNumber } from "../../../components/utils";
import { CURR_YEAR, RPMapping } from "../../../constants";
import { round, truncate } from "../../../utils";
import { TeamYearData } from "../types";

export type TeamYearInsights = {
  num: number;
  team: string;
  epa_rank: number;
  norm_epa: number;
  total_epa: number; // used for sorting
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
  record: string;
};

const columnHelper = createColumnHelper<TeamYearInsights>();

const defaultFilters = {
  country: "",
  state: "",
  district: "",
};

const PageTeamInsightsTable = ({ year, data }: { year: number; data: TeamYearData }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [filters, setFilters] = useState(defaultFilters);

  const yearInsightsData: TeamYearInsights[] = filterData(data.team_years, filters)
    .map((teamYear: APITeamYear) => {
      return {
        num: teamYear.num ?? -1,
        team: teamYear.team ? truncate(teamYear.team, 30) : "N/A",
        epa_rank: teamYear.epa_rank ?? -1,
        norm_epa: round(teamYear.norm_epa, 0) ?? 0,
        total_epa: round(teamYear.total_epa, 1) ?? 0,
        auto_epa: round(teamYear.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamYear.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamYear.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamYear.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamYear.rp_2_epa, 2) ?? "N/A",
        record: `${teamYear.wins}-${teamYear.losses}-${teamYear.ties}` ?? "N/A",
      };
    })
    .sort((a, b) => b.norm_epa - a.norm_epa);

  const columns = useMemo<any>(() => {
    const showColumns = [
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num }),
        header: "Name",
      }),
      columnHelper.accessor("epa_rank", {
        cell: (info) => formatCell(info),
        header: "EPA Rank",
      }),
      year < CURR_YEAR &&
        columnHelper.accessor("norm_epa", {
          cell: (info) => formatCell(info),
          header: "Normalized EPA",
        }),
      columnHelper.accessor("total_epa", {
        cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      year >= 2016 &&
        columnHelper.accessor("auto_epa", {
          cell: (info) => formatPercentileCell(data.year.auto_stats, info, disableHighlight),
          header: "Auto EPA",
        }),
      year >= 2016 &&
        columnHelper.accessor("teleop_epa", {
          cell: (info) => formatPercentileCell(data.year.teleop_stats, info, disableHighlight),
          header: "Teleop EPA",
        }),
      year >= 2016 &&
        columnHelper.accessor("endgame_epa", {
          cell: (info) => formatPercentileCell(data.year.endgame_stats, info, disableHighlight),
          header: "Endgame EPA",
        }),
      year >= 2016 &&
        columnHelper.accessor("rp_1_epa", {
          cell: (info) => formatPercentileCell(data.year.rp_1_stats, info, disableHighlight),
          header: `${RPMapping[year][0]} EPA`,
        }),
      year >= 2016 &&
        columnHelper.accessor("rp_2_epa", {
          cell: (info) => formatPercentileCell(data.year.rp_2_stats, info, disableHighlight),
          header: `${RPMapping[year][1]} EPA`,
        }),
      columnHelper.accessor("record", {
        cell: (info) => formatCell(info),
        header: "Record",
      }),
    ].filter((x) => x);
    return showColumns;
  }, [year, data.year, disableHighlight]);

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="flex items-center justify-center mb-4">
        <FilterBar defaultFilters={defaultFilters} filters={filters} setFilters={setFilters} />
      </div>
      <InsightsTable
        data={yearInsightsData}
        columns={columns}
        leftCol="num"
        rightCol="record"
        searchCols={["num", "team"]}
        csvFilename={`${year}_insights.csv`}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </div>
  );
};

export default PageTeamInsightsTable;
