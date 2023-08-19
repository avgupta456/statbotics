"use client";

import React, { useMemo } from "react";

import Link from "next/link";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import { classnames, truncate } from "../../utils";
import { APIYear, PercentileStats } from "../types/api";
import { formatNumber } from "../utils";
import Table from "./Table";
import { CONDITIONAL_COLORS, getEPAColor } from "./shared";

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

const columnHelper = createColumnHelper<Component>();

// Copied from ./shared.tsx with minor changes

const TeamLink = ({ team, num, year }: { team: string | number; num: number; year: number }) => {
  if (num > 100000) {
    return formatNumber(num);
  } else {
    return (
      <div className="w-24 h-full flex justify-center items-center">
        <Link href={`/team/${num}/${year}`} className="text_link">
          {truncate(team.toString(), 30)}
        </Link>
      </div>
    );
  }
};

const formatCell = (
  stats: APIYear,
  info: CellContext<Component, number | string>,
  multiplier: number = 1
) => {
  const row = info.row.original.name;
  const value = info.getValue();

  let color = "";
  if (typeof value === "string" || row == "Fouls") {
    color = CONDITIONAL_COLORS[1];
  } else {
    const percentileStats: PercentileStats =
      row === "Auto"
        ? stats.auto_stats
        : row === "Teleop"
        ? stats.teleop_stats
        : row === "Endgame"
        ? stats.endgame_stats
        : row === "RP1"
        ? stats.rp_1_stats
        : row === "RP2"
        ? stats.rp_2_stats
        : stats.total_stats;

    color = getEPAColor(value, percentileStats, multiplier);
  }

  return (
    <div className="w-22 h-full flex justify-center items-center">
      <div className={classnames(color, "data w-12 px-2 py-1 rounded-lg")}>{info.getValue()}</div>
    </div>
  );
};

const MatchBreakdown = ({
  data,
  teams,
  stats,
}: {
  data: Component[];
  teams: number[];
  stats: APIYear;
}) => {
  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("red1", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[0], num: teams[0], year: stats.year }),
        enableSorting: false,
      }),
      columnHelper.accessor("red2", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[1], num: teams[1], year: stats.year }),
        enableSorting: false,
      }),
      columnHelper.accessor("red3", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[2], num: teams[2], year: stats.year }),
        enableSorting: false,
      }),
      columnHelper.accessor("redTotal", {
        cell: (info) => formatCell(stats, info, 3),
        header: () => <span>Predicted</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("redActual", {
        cell: (info) => formatCell(stats, info, 3),
        header: () => <span>Actual</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("name", {
        cell: (info) => info.getValue(),
        header: () => <span></span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blueActual", {
        cell: (info) => formatCell(stats, info, 3),
        header: () => <span>Actual</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blueTotal", {
        cell: (info) => formatCell(stats, info, 3),
        header: () => <span>Predicted</span>,
        enableSorting: false,
      }),
      columnHelper.accessor("blue3", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[5], num: teams[5], year: stats.year }),
        enableSorting: false,
      }),
      columnHelper.accessor("blue2", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[4], num: teams[4], year: stats.year }),
        enableSorting: false,
      }),
      columnHelper.accessor("blue1", {
        cell: (info) => formatCell(stats, info),
        header: () => TeamLink({ team: teams[3], num: teams[3], year: stats.year }),
        enableSorting: false,
      }),
    ],
    [stats, teams]
  );

  const headerClassName = () => "border-b-2";

  const headerCellClassName = (header: any) =>
    classnames(
      "w-24 p-2",
      header.id.includes("red") ? "bg-red-200" : "",
      header.id.includes("blue") ? "bg-blue-200" : "",
      header.id.includes("name") ? "bg-gray-100" : "",
      header.id === "red1" ? "rounded-tl-lg" : "",
      header.id === "blue1" ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-full",
      row.original.name === "Total" ? "font-bold bg-gray-300" : "hover:bg-blue-100"
    );

  const cellClassName = (cell: any) =>
    classnames(
      "w-24 py-2",
      ["redTotal", "blueTotal", "name"].includes(cell.column.id) ? "border-l-2 border-r-2" : "",
      cell.row.original.name === "Total" && cell.column.id === "red1" ? "rounded-bl-lg" : "",
      cell.row.original.name === "Total" && cell.column.id === "blue1" ? "rounded-br-lg" : ""
    );

  return (
    <Table
      data={data}
      columns={columns}
      paginate={false}
      headerClassName={headerClassName}
      headerCellClassName={headerCellClassName}
      rowClassName={rowClassName}
      cellClassName={cellClassName}
    />
  );
};

export default MatchBreakdown;
