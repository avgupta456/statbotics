"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatPercentileCell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { CURR_YEAR, RPMapping } from "../../../../constants";
import { round, truncate } from "../../../../utils";
import { Data } from "./types";

export type TeamEventInsights = {
  num: number;
  team: string;
  rank: number;
  unitless_epa: number | string;
  norm_epa: number | string;
  total_epa: number;
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
};

const columnHelper = createColumnHelper<TeamEventInsights>();

const PageEventInsightsTable = ({ eventId, data }: { eventId: string; data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const eventInsightsData: TeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent.num ?? -1,
        team: teamEvent.team ? truncate(teamEvent.team, 30) : "N/A",
        unitless_epa: round(teamEvent.unitless_epa, 0) ?? "N/A",
        norm_epa: round(teamEvent.norm_epa, 0) ?? "N/A",
        total_epa: round(teamEvent.total_epa, 1) ?? 0,
        auto_epa: round(teamEvent.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamEvent.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamEvent.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamEvent.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamEvent.rp_2_epa, 2) ?? "N/A",
        rank: teamEvent.rank ?? -1,
      };
    })
    .sort((a, b) => a.rank - b.rank || b.total_epa - a.total_epa);

  const maxRank = Math.max(...eventInsightsData.map((team) => team.rank));

  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("num", {
          cell: (info) => formatNumber(info.getValue()),
          header: "Number",
        }),
        columnHelper.accessor("team", {
          cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num }),
          header: "Name",
        }),
        maxRank > 0 &&
          columnHelper.accessor("rank", {
            cell: (info) => formatCell(info),
            header: "Rank",
          }),
        data.year.year >= CURR_YEAR &&
          columnHelper.accessor("unitless_epa", {
            cell: (info) => formatCell(info),
            header: "Unitless EPA",
          }),
        data.year.year < CURR_YEAR &&
          columnHelper.accessor("norm_epa", {
            cell: (info) => formatCell(info),
            header: "Norm EPA",
          }),
        columnHelper.accessor("total_epa", {
          cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
          header: "EPA",
        }),
        data.year.year >= 2016 &&
          columnHelper.accessor("auto_epa", {
            cell: (info) => formatPercentileCell(data.year.auto_stats, info, disableHighlight),
            header: "Auto EPA",
          }),
        data.year.year >= 2016 &&
          columnHelper.accessor("teleop_epa", {
            cell: (info) => formatPercentileCell(data.year.teleop_stats, info, disableHighlight),
            header: "Teleop EPA",
          }),
        data.year.year >= 2016 &&
          columnHelper.accessor("endgame_epa", {
            cell: (info) => formatPercentileCell(data.year.endgame_stats, info, disableHighlight),
            header: "Endgame EPA",
          }),
        data.year.year >= 2016 &&
          columnHelper.accessor("rp_1_epa", {
            cell: (info) => formatPercentileCell(data.year.rp_1_stats, info, disableHighlight),
            header: `${RPMapping?.[data.year.year]?.[0]} EPA`,
          }),
        data.year.year >= 2016 &&
          columnHelper.accessor("rp_2_epa", {
            cell: (info) => formatPercentileCell(data.year.rp_2_stats, info, disableHighlight),
            header: `${RPMapping?.[data.year.year]?.[1]} EPA`,
          }),
      ].filter(Boolean),
    [data, maxRank, disableHighlight]
  );

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <InsightsTable
        data={eventInsightsData}
        columns={columns}
        leftCol="num"
        rightCol="rp_2_epa"
        searchCols={["num", "team"]}
        csvFilename={`${eventId}_team_insights.csv`}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </div>
  );
};

export default PageEventInsightsTable;
