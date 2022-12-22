"use client";

import React, { useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import {
  Stats,
  TeamLink,
  formatCell,
  headerClassName,
  rowClassName,
  cellClassName,
} from "./MatchTables";
import Table from "./Table";

export type PredComponent = {
  name: string;
  red1: number | null;
  red2: number | null;
  red3: number | null;
  redTotal: number | null;
  blue1: number | null;
  blue2: number | null;
  blue3: number | null;
  blueTotal: number | null;
};

const MatchPredictionTable = ({
  data,
  teams,
  stats,
}: {
  data: PredComponent[];
  teams: string[];
  stats: Stats;
}) => {
  const columnHelper = createColumnHelper<PredComponent>();

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
      header: () => <span>Total</span>,
    }),
    columnHelper.accessor("name", {
      cell: (info) => info.getValue(),
      header: () => <span></span>,
    }),
    columnHelper.accessor("blueTotal", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Total</span>,
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

  return Table(data, columns, headerClassName, rowClassName, cellClassName);
};

export default MatchPredictionTable;
