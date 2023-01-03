"use client";

import React, { useMemo } from "react";

import { CellContext, createColumnHelper } from "@tanstack/react-table";

import { classnames } from "../../utils";
import { formatNumber } from "../utils";
import Table from "./Table";
import { TeamLink } from "./shared";

export type SimulationRow = {
  rank: number;
  num: number;
  team: string;
  rankMean: number;
  rank5: number;
  rank50: number;
  rank95: number;
  RPMean: number;
};

const columnHelper = createColumnHelper<SimulationRow>();

const SimulationTable = ({ data }: { data: SimulationRow[] }) => {
  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("rank", {
        cell: (info) => info.getValue(),
        header: "Predicted Rank",
      }),
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num }),
        header: "Team",
      }),
      columnHelper.accessor("rankMean", {
        cell: (info) => info.getValue(),
        header: "Mean Rank",
      }),
      columnHelper.accessor("rank5", {
        cell: (info) => info.getValue(),
        header: "5% Rank",
      }),
      columnHelper.accessor("rank50", {
        cell: (info) => info.getValue(),
        header: "Median Rank",
      }),
      columnHelper.accessor("rank95", {
        cell: (info) => info.getValue(),
        header: "95% Rank",
      }),
      columnHelper.accessor("RPMean", {
        cell: (info) => info.getValue(),
        header: "Mean RPs",
      }),
    ],
    []
  );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) =>
    classnames(
      "w-28 p-2",
      header.id === "rank" ? "rounded-tl-lg" : "",
      header.id === "RPMean" ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) => classnames("text-center h-full hover:bg-blue-100");

  const cellClassName = (cell: any) =>
    classnames(
      cell.column.id === "team" ? "w-40 py-2 truncate" : "w-28 py-2",
      cell.row.index === data.length - 1 && cell.column.id === "rank" ? "rounded-bl-lg" : "",
      cell.row.index === data.length - 1 && cell.column.id === "RPMean" ? "rounded-br-lg" : ""
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

export default SimulationTable;
