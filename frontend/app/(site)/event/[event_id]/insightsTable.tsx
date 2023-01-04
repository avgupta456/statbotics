"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { RPMapping } from "../../../../constants";
import { round, truncate } from "../../../../utils";
import { Data } from "./types";

export type TeamEventInsights = {
  num: number;
  team: string;
  rank: number | string;
  total_epa: number | string;
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

  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num }),
        header: "Name",
      }),
      columnHelper.accessor("rank", {
        cell: (info) => info.getValue(),
        header: "Rank",
      }),
      columnHelper.accessor("total_epa", {
        cell: (info) => formatCell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      columnHelper.accessor("auto_epa", {
        cell: (info) => formatCell(data.year.auto_stats, info, disableHighlight),
        header: "Auto EPA",
      }),
      columnHelper.accessor("teleop_epa", {
        cell: (info) => formatCell(data.year.teleop_stats, info, disableHighlight),
        header: "Teleop EPA",
      }),
      columnHelper.accessor("endgame_epa", {
        cell: (info) => formatCell(data.year.endgame_stats, info, disableHighlight),
        header: "Endgame EPA",
      }),
      columnHelper.accessor("rp_1_epa", {
        cell: (info) => formatCell(data.year.rp_1_stats, info, disableHighlight),
        header: `${RPMapping[data.year.year][0]} EPA`,
      }),
      columnHelper.accessor("rp_2_epa", {
        cell: (info) => formatCell(data.year.rp_2_stats, info, disableHighlight),
        header: `${RPMapping[data.year.year][1]} EPA`,
      }),
    ],
    [data, disableHighlight]
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
