"use client";

import React, { useState } from "react";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import Table from "./Table";
import { TeamLink, CONDITIONAL_COLORS, getColor, getRPColor } from "./shared";
import { YearStats } from "../types/api";
import { classnames } from "../../utils";

export type TeamEventInsights = {
  num: number;
  team: string;
  rank: number | null;
  epa: number | null;
  auto_epa: number | null;
  teleop_epa: number | null;
  endgame_epa: number | null;
  rp_1_epa: number | null;
  rp_2_epa: number | null;
};

type CleanTeamEventInsights = {
  num: number;
  team: string;
  rank: number | string;
  epa: number | string;
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
};

const formatCell = (
  mean: number,
  info: CellContext<CleanTeamEventInsights, number | string>
) => {
  const column = info.column.id;
  const value = info.getValue();

  let color = "";
  if (typeof value === "string") {
    color = CONDITIONAL_COLORS[1];
  } else {
    const compValue =
      column == "rp_1_epa" || column == "rp_2_epa" ? value + 1 / 3 : value;
    color = getColor(compValue, mean);
  }

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div
        className={classnames(
          color,
          "data w-6 lg:w-12 p-0.5 lg:p-1 rounded lg:rounded-lg"
        )}
      >
        {info.getValue()}
      </div>
    </div>
  );
};

const EventInsightsTable = ({
  data,
  stats,
}: {
  data: TeamEventInsights[];
  stats: YearStats;
}) => {
  const columnHelper = createColumnHelper<CleanTeamEventInsights>();

  const columns = [
    columnHelper.accessor("num", {
      cell: (info) => info.getValue(),
      header: "Number",
    }),
    columnHelper.accessor("team", {
      cell: (info) => TeamLink({ team: info.getValue() }),
      header: "Name",
    }),
    columnHelper.accessor("rank", {
      cell: (info) => info.getValue(),
      header: "Rank",
    }),
    columnHelper.accessor("epa", {
      cell: (info) => formatCell(stats.total_mean / 3, info),
      header: "EPA",
    }),
    columnHelper.accessor("auto_epa", {
      cell: (info) => formatCell(stats.auto_mean / 3, info),
      header: "Auto EPA",
    }),
    columnHelper.accessor("teleop_epa", {
      cell: (info) => formatCell(stats.teleop_mean / 3, info),
      header: "Teleop EPA",
    }),
    columnHelper.accessor("endgame_epa", {
      cell: (info) => formatCell(stats.endgame_mean / 3, info),
      header: "Endgame EPA",
    }),
    columnHelper.accessor("rp_1_epa", {
      cell: (info) => formatCell(stats.rp_1_mean / 3, info),
      header: "RP1 EPA",
    }),
    columnHelper.accessor("rp_2_epa", {
      cell: (info) => formatCell(stats.rp_2_mean / 3, info),
      header: "RP2 EPA",
    }),
  ];

  const headerClassName = (header: any) =>
    classnames(
      "w-28 py-2",
      header.id === "num" ? "rounded-tl-lg" : "",
      header.id === "rp_2_epa" ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-full hover:bg-blue-100",
      row.index % 2 === 0 ? "" : "bg-gray-100"
    );

  const cellClassName = (cell: any) =>
    classnames(
      "w-28 py-2",
      cell.row.index === data.length - 1 && cell.column.id === "num"
        ? "rounded-bl-lg"
        : "",
      cell.row.index === data.length - 1 && cell.column.id === "rp_2_epa"
        ? "rounded-br-lg"
        : ""
    );

  return Table(data, columns, headerClassName, rowClassName, cellClassName);
};

export default EventInsightsTable;
