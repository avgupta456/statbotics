"use client";

import React, { useMemo } from "react";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import { classnames } from "../../utils";
import { APIYear, PercentileStats } from "../types/api";
import { formatNumber } from "../utils";
import Table from "./Table";
import { CONDITIONAL_COLORS, TeamLink, getColor, getRPColor } from "./shared";

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

const formatCell = (
  percentileStats: PercentileStats,
  info: CellContext<TeamEventInsights, number | string>,
  disableHighlight: boolean
) => {
  const column = info.column.id;
  const value = info.getValue();

  let color = "";
  if (disableHighlight) {
    color = "";
  } else if (typeof value === "string") {
    color = CONDITIONAL_COLORS[1];
  } else if (column == "rp_1_epa" || column == "rp_2_epa") {
    color = getRPColor(value);
  } else {
    color = getColor(value, percentileStats);
  }

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div className={classnames(color, "data w-6 lg:w-12 p-0.5 lg:m-0.5 rounded lg:rounded-lg")}>
        {info.getValue()}
      </div>
    </div>
  );
};

const columnHelper = createColumnHelper<TeamEventInsights>();

const EventInsightsTable = ({
  data,
  stats,
  disableHighlight,
}: {
  data: TeamEventInsights[];
  stats: APIYear;
  disableHighlight: boolean;
}) => {
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
        cell: (info) => formatCell(stats.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      columnHelper.accessor("auto_epa", {
        cell: (info) => formatCell(stats.auto_stats, info, disableHighlight),
        header: "Auto EPA",
      }),
      columnHelper.accessor("teleop_epa", {
        cell: (info) => formatCell(stats.teleop_stats, info, disableHighlight),
        header: "Teleop EPA",
      }),
      columnHelper.accessor("endgame_epa", {
        cell: (info) => formatCell(stats.endgame_stats, info, disableHighlight),
        header: "Endgame EPA",
      }),
      columnHelper.accessor("rp_1_epa", {
        cell: (info) => formatCell(stats.rp_1_stats, info, disableHighlight),
        header: "RP1 EPA",
      }),
      columnHelper.accessor("rp_2_epa", {
        cell: (info) => formatCell(stats.rp_2_stats, info, disableHighlight),
        header: "RP2 EPA",
      }),
    ],
    [stats, disableHighlight]
  );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) =>
    classnames(
      "w-28 py-2",
      header.id === "num" ? "rounded-tl-lg" : "",
      header.id === "rp_2_epa" ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) => classnames("text-center h-full hover:bg-blue-100");

  const cellClassName = (cell: any) =>
    classnames(
      cell.column.id === "team" ? "w-40 py-2 truncate" : "w-28 py-2",
      cell.row.index === data.length - 1 && cell.column.id === "num" ? "rounded-bl-lg" : "",
      cell.row.index === data.length - 1 && cell.column.id === "rp_2_epa" ? "rounded-br-lg" : ""
    );

  return Table(
    data,
    columns,
    true,
    headerClassName,
    headerCellClassName,
    rowClassName,
    cellClassName
  );
};

export default EventInsightsTable;
