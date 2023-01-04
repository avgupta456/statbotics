import React from "react";

import Link from "next/link";

import { CellContext } from "@tanstack/react-table";

import { classnames, round } from "../../utils";
import { PercentileStats } from "../types/api";
import { formatNumber } from "../utils";

export const TeamLink = ({ team, num }: { team: string | number; num: number }) => {
  if (num > 100000) {
    return formatNumber(num);
  } else {
    return (
      <Link href={`/team/${num}`} className="text_link">
        {team}
      </Link>
    );
  }
};

export const CONDITIONAL_COLORS = [
  "text-red-700 bg-red-100",
  "text-gray-800",
  "text-green-800 bg-green-50",
  "text-green-800 bg-green-100",
  "text-blue-800 bg-blue-200",
];

export const getColor = (
  value: number,
  percentileStats: PercentileStats,
  multiplier: number = 1
) => {
  let color = "";
  if (value < multiplier * percentileStats.p25) {
    color = CONDITIONAL_COLORS[0];
  } else if (value < multiplier * percentileStats.p75) {
    color = CONDITIONAL_COLORS[1];
  } else if (value < multiplier * percentileStats.p90) {
    color = CONDITIONAL_COLORS[2];
  } else if (value < multiplier * percentileStats.p99) {
    color = CONDITIONAL_COLORS[3];
  } else {
    color = CONDITIONAL_COLORS[4];
  }

  return color;
};

export const getRPColor = (value: number) => {
  let color = "";
  if (value < 0.5) {
    color = CONDITIONAL_COLORS[1];
  } else if (value < 0.75) {
    color = CONDITIONAL_COLORS[2];
  } else if (value <= 1) {
    color = CONDITIONAL_COLORS[3];
  } else {
    color = CONDITIONAL_COLORS[4];
  }
  return color;
};

export const formatCell = (
  percentileStats: PercentileStats,
  info: CellContext<any, number | string>,
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

export const TableKey = () => (
  <div className="w-full flex justify-center items-center text-xs my-4">
    <p className="text-sm">Key (Percentile):</p>
    {[
      { color: CONDITIONAL_COLORS[0], text: "0 - 25" },
      { color: CONDITIONAL_COLORS[1], text: "25 - 75" },
      { color: CONDITIONAL_COLORS[2], text: "75 - 90" },
      { color: CONDITIONAL_COLORS[3], text: "90 - 99" },
      { color: CONDITIONAL_COLORS[4], text: "99 - 100" },
    ].map((item) => (
      <span
        key={item.color}
        className={classnames(
          item.color,
          "data w-16 p-1 ml-4 rounded lg:rounded-lg flex justify-center items-center"
        )}
      >
        {item.text}
      </span>
    ))}
  </div>
);
