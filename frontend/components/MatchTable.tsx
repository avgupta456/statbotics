"use client";

import React, { useState } from "react";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import Table from "./Table";
import { classnames } from "../utils";

export type Component = {
  name: string;
  red1: number | null;
  red2: number | null;
  red3: number | null;
  redTotal: number | null;
  redActual: number | null;
  blue1: number | null;
  blue2: number | null;
  blue3: number | null;
  blueTotal: number | null;
  blueActual: number | null;
};

type CleanComponent = {
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

// Copied from frontend\app\match\[match_id]\types.tsx
type YearStats = {
  auto_mean: number;
  teleop_mean: number;
  endgame_mean: number;
  total_mean: number;
  foul_rate: number;
  rp_1_mean: number;
  rp_2_mean: number;
};

const TeamLink = ({ team }: { team: string }) => (
  <a
    href={`/team/${team}`}
    target="_blank"
    rel="noopener noreferrer"
    className="text-blue-500 hover:text-blue-600 underline cursor-pointer"
  >
    {team}
  </a>
);

const CONDITIONAL_COLORS = [
  "text-red-700 bg-red-300",
  "text-gray-800 bg-gray-200",
  "text-green-500 bg-green-100",
  "text-green-700 bg-green-300",
  "text-black bg-green-500",
  "text-blue-500 bg-blue-100",
  "text-blue-700 bg-blue-300",
  "text-white bg-blue-500",
];

const getColor = (value: number, mean: number) => {
  let color = "";
  if (value < 0.5 * mean) {
    color = CONDITIONAL_COLORS[0];
  } else if (value < 1.5 * mean) {
    color = CONDITIONAL_COLORS[1];
  } else if (value < 2 * mean) {
    color = CONDITIONAL_COLORS[2];
  } else if (value < 3 * mean) {
    color = CONDITIONAL_COLORS[3];
  } else if (value < 4 * mean) {
    color = CONDITIONAL_COLORS[4];
  } else if (value < 5 * mean) {
    color = CONDITIONAL_COLORS[5];
  } else if (value < 6 * mean) {
    color = CONDITIONAL_COLORS[6];
  } else {
    color = CONDITIONAL_COLORS[7];
  }

  return color;
};

const getRPColor = (value: number, mean: number) => {
  let color = "";
  if (value < 0.25) {
    color = CONDITIONAL_COLORS[0];
  } else if (value < 0.5) {
    color = CONDITIONAL_COLORS[1];
  } else if (value < 0.75) {
    color = CONDITIONAL_COLORS[2];
  } else if (value < 0.9) {
    color = CONDITIONAL_COLORS[3];
  } else {
    color = CONDITIONAL_COLORS[4];
  }
  return color;
};

const formatCell = (
  stats: YearStats,
  info: CellContext<CleanComponent, number | string>,
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

    if (
      row.includes("RP") &&
      (column.includes("Total") || column.includes("Actual"))
    ) {
      color = getRPColor(compValue, mean);
    } else {
      color = getColor(compValue, mean);
    }
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

const MatchTable = ({
  data,
  teams,
  stats,
}: {
  data: Component[];
  teams: string[];
  stats: YearStats;
}) => {
  const columnHelper = createColumnHelper<CleanComponent>();

  const columns = [
    columnHelper.accessor("red1", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[0] }),
    }),
    columnHelper.accessor("red2", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[1] }),
    }),
    columnHelper.accessor("red3", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[2] }),
    }),
    columnHelper.accessor("redTotal", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Predicted</span>,
    }),
    columnHelper.accessor("redActual", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Actual</span>,
    }),
    columnHelper.accessor("name", {
      cell: (info) => info.getValue(),
      header: () => <span></span>,
    }),
    columnHelper.accessor("blueActual", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Actual</span>,
    }),
    columnHelper.accessor("blueTotal", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Predicted</span>,
    }),
    columnHelper.accessor("blue3", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[5] }),
    }),
    columnHelper.accessor("blue2", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[4] }),
    }),
    columnHelper.accessor("blue1", {
      cell: (info) => formatCell(stats, info),
      header: () => TeamLink({ team: teams[3] }),
    }),
  ];

  const headerClassName = (header: any) =>
    classnames(
      "w-24 py-2",
      header.colSpan > 1 ? "border-b-2" : "",
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
      row.original.name === "Total"
        ? "font-bold bg-gray-300"
        : "hover:bg-blue-100"
    );

  const cellClassName = (cell: any) =>
    classnames(
      "w-24 py-2",
      ["redTotal", "blueTotal", "name"].includes(cell.column.id)
        ? "border-l-2 border-r-2"
        : "",
      cell.row.original.name === "Total" && cell.column.id === "red1"
        ? "rounded-bl-lg"
        : "",
      cell.row.original.name === "Total" && cell.column.id === "blue1"
        ? "rounded-br-lg"
        : ""
    );

  return Table(data, columns, headerClassName, rowClassName, cellClassName);
};

export default MatchTable;
