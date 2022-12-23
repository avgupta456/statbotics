"use client";

import React, { useMemo, useState } from "react";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import { classnames } from "../../utils";
import { YearStats } from "../types/api";
import Table from "./Table";
import { CONDITIONAL_COLORS, TeamLink, getColor, getRPColor } from "./shared";

export type Component = {
  name: string;
  red1: number | string;
  red2: number | string;
  red3: number | string;
  redTotal: number | string;
  redActual: number | string;
  blue1: number | string;
  blue2: number | string;
  blue3: number | string;
  blueTotal: number | string;
  blueActual: number | string;
};

const formatCell = (
  stats: YearStats,
  info: CellContext<Component, number | string>,
  multiplier: number = 1 / 3
) => {
  const row = info.row.original.name;
  const column = info.column.id;
  const value = info.getValue();

  let color = "";
  if (typeof value === "string" || row == "Fouls") {
    color = CONDITIONAL_COLORS[1];
  } else {
    const compValue = row == "RP1" || row == "RP2" ? value + 1 / 3 : value;
    const mean =
      multiplier *
      (row === "Auto"
        ? stats.auto_mean
        : row === "Teleop"
        ? stats.teleop_mean
        : row === "Endgame"
        ? stats.endgame_mean
        : row === "RP1"
        ? stats.rp_1_mean
        : row === "RP2"
        ? stats.rp_2_mean
        : stats.total_mean);

    if (row.includes("RP") && (column.includes("Total") || column.includes("Actual"))) {
      color = getRPColor(compValue, mean);
    } else {
      color = getColor(compValue, mean);
    }
  }

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div className={classnames(color, "data w-6 lg:w-12 p-0.5 lg:p-1 rounded lg:rounded-lg")}>
        {info.getValue()}
      </div>
    </div>
  );
};

const columnHelper = createColumnHelper<Component>();

const MatchTable = ({
  data,
  teams,
  stats,
}: {
  data: Component[];
  teams: string[];
  stats: YearStats;
}) => {
  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("red1", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[0], num: teams[0] }),
        enableSorting: false,
      }),
      columnHelper.accessor("red2", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[1], num: teams[1] }),
        enableSorting: false,
      }),
      columnHelper.accessor("red3", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[2], num: teams[2] }),
        enableSorting: false,
      }),
      columnHelper.accessor("redTotal", {
        cell: (info) => formatCell(stats, info, 1),
        header: () => <span>Predicted</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("redActual", {
        cell: (info) => formatCell(stats, info, 1),
        header: () => <span>Actual</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("name", {
        cell: (info) => info.getValue(),
        header: () => <span></span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blueActual", {
        cell: (info) => formatCell(stats, info, 1),
        header: () => <span>Actual</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blueTotal", {
        cell: (info) => formatCell(stats, info, 1),
        header: () => <span>Predicted</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blue3", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[5], num: teams[5] }),
        enableSorting: false,
      }),
      columnHelper.accessor("blue2", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[4], num: teams[4] }),
        enableSorting: false,
      }),
      columnHelper.accessor("blue1", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[3], num: teams[3] }),
        enableSorting: false,
      }),
    ],
    [stats, teams]
  );

  const headerClassName = (header: any) =>
    classnames(
      "w-24 py-2",
      header.id.includes("red") ? "bg-red-200" : "",
      header.id.includes("blue") ? "bg-blue-200" : "",
      header.id.includes("name") ? "bg-gray-100" : "",
      header.id === "red1" ? "rounded-tl-lg" : "",
      header.id === "blue1" ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-full",
      row.index % 2 === 0 ? "" : "bg-gray-100",
      row.original.name === "Total" ? "font-bold bg-gray-300" : "hover:bg-blue-100"
    );

  const cellClassName = (cell: any) =>
    classnames(
      "w-24 py-2",
      ["redTotal", "blueTotal", "name"].includes(cell.column.id) ? "border-l-2 border-r-2" : "",
      cell.row.original.name === "Total" && cell.column.id === "red1" ? "rounded-bl-lg" : "",
      cell.row.original.name === "Total" && cell.column.id === "blue1" ? "rounded-br-lg" : ""
    );

  return Table(data, columns, headerClassName, rowClassName, cellClassName);
};

export default MatchTable;
