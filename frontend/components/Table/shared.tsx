import React from "react";

import Link from "next/link";

import { classnames } from "../../utils";
import { PercentileStats } from "../types/api";

export const TeamLink = ({ team, num }: { team: string | number; num: string | number }) => (
  <Link href={`/team/${num}`} className="text_link">
    {team}
  </Link>
);

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
