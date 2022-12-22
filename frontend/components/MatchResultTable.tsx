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

export type ResultComponent = {
  name: string;
  redPred: number | null;
  redActual: number | null;
  bluePred: number | null;
  blueActual: number | null;
};

const MatchPredictionTable = ({
  data,
  stats,
}: {
  data: ResultComponent[];
  stats: Stats;
}) => {
  const columnHelper = createColumnHelper<ResultComponent>();

  const columns = [
    columnHelper.accessor("redPred", {
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
    columnHelper.accessor("bluePred", {
      cell: (info) => formatCell(stats, info, 1),
      header: () => <span>Predicted</span>,
    }),
  ];

  return Table(data, columns, headerClassName, rowClassName, cellClassName);
};

export default MatchPredictionTable;
