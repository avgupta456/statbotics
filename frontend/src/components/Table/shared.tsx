import React from "react";

import Link from "next/link";

import { CellContext } from "@tanstack/react-table";

import { EPAPercentiles } from "../../types/api";
import { classnames, truncate } from "../../utils";

export const TeamLink = ({
  team,
  num,
  year,
  small,
}: {
  team: string;
  num: number;
  year: number;
  small?: boolean;
}) => {
  return (
    <div
      className={classnames(
        "mx-auto h-10 h-full flex justify-center items-center text-sm",
        small ? "w-16 md:w-20" : "w-24 md:w-32"
      )}
    >
      <Link href={`/team/${num}/${year}`} className="text_link">
        {truncate(team.toString(), 30)}
      </Link>
    </div>
  );
};

export const EventLink = ({ key, event }: { key: string; event: string }) => {
  if (event === "N/A") {
    return (
      <div className="w-32 md:w-40 mx-auto h-full flex justify-center items-center text-sm">
        {event}
      </div>
    );
  }

  return (
    <div className="w-32 md:w-40 mx-auto h-full flex justify-center items-center text-sm">
      <Link href={`/event/${key}`} className="text_link">
        {truncate(event.toString(), 40)}
      </Link>
    </div>
  );
};

export const CONDITIONAL_COLORS = [
  "text-red-700 bg-red-100",
  "text-gray-800",
  "text-green-800 bg-green-50",
  "text-green-800 bg-green-100",
  "text-blue-800 bg-blue-200",
];

export const getEPAColor = (
  value: number,
  percentileStats: EPAPercentiles,
  multiplier: number = 1,
  reverse: boolean = false
) => {
  let color = "";

  if (reverse) {
    if (value > multiplier * percentileStats?.p25 || 0) {
      color = CONDITIONAL_COLORS[0];
    } else if (value > multiplier * percentileStats?.p75 || 0) {
      color = CONDITIONAL_COLORS[1];
    } else if (value > multiplier * percentileStats?.p90 || 0) {
      color = CONDITIONAL_COLORS[2];
    } else if (value > multiplier * percentileStats?.p99 || 0) {
      color = CONDITIONAL_COLORS[3];
    } else {
      color = CONDITIONAL_COLORS[4];
    }
  } else {
    if (value < multiplier * percentileStats?.p25 || 0) {
      color = CONDITIONAL_COLORS[0];
    } else if (value < multiplier * percentileStats?.p75 || 0) {
      color = CONDITIONAL_COLORS[1];
    } else if (value < multiplier * percentileStats?.p90 || 0) {
      color = CONDITIONAL_COLORS[2];
    } else if (value < multiplier * percentileStats?.p99 || 0) {
      color = CONDITIONAL_COLORS[3];
    } else {
      color = CONDITIONAL_COLORS[4];
    }
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

export const formatCell = (info: CellContext<any, number | string>) => {
  const value = info.getValue();

  return (
    <div className="w-16 md:w-20 mx-auto h-full flex justify-center items-center">{value}</div>
  );
};

export const formatEPACell = (
  percentileStats: EPAPercentiles,
  info: CellContext<any, number | string>,
  disableHighlight: boolean,
  multiplier: number = 1,
  reverse: boolean = false
) => {
  const column = info.column.id;
  const value = info.getValue();

  let color = "";
  if (disableHighlight) {
    color = "";
  } else if (typeof value === "string") {
    color = CONDITIONAL_COLORS[1];
  } else if (column == "rp_1_epa" || column == "rp_2_epa" || column == "rp_3_epa") {
    color = getRPColor(value);
  } else {
    color = getEPAColor(value, percentileStats, multiplier, reverse);
  }

  return (
    <div className="w-16 md:w-20 mx-auto h-full flex justify-center items-center">
      <div className={classnames(color, "w-12 px-2 py-1 rounded-lg")}>{info.getValue()}</div>
    </div>
  );
};

export const formatProbCell = (info: CellContext<any, number>) => {
  const value = info.getValue();

  let color = "";
  if (value < 0.05) {
    color = CONDITIONAL_COLORS[1];
  } else if (value < 0.1) {
    color = CONDITIONAL_COLORS[2];
  } else if (value < 0.25) {
    color = CONDITIONAL_COLORS[3];
  } else if (value < 0.5) {
    color = "text-green-800 bg-green-200";
  } else if (value >= 0.5) {
    color = CONDITIONAL_COLORS[4];
  }

  return (
    <div className="w-16 mx-auto h-full flex justify-center items-center">
      <div className={classnames(color, "w-12 px-2 py-1 rounded-lg")}>
        {value ? value.toFixed(2) : ""}
      </div>
    </div>
  );
};

export const formatPercentileCell = (info: CellContext<any, number>, disableHighlight: boolean) => {
  const value = info.getValue();

  let color = "";
  if (disableHighlight) {
  } else if (value < 1 / 3) {
    color = CONDITIONAL_COLORS[3];
  } else if (value > 2 / 3) {
    color = CONDITIONAL_COLORS[0];
  }

  return (
    <div className="w-16 mx-auto h-full flex justify-center items-center">
      <div className={classnames(color, "w-12 px-2 py-1 rounded-lg")}>{value?.toFixed(2)}</div>
    </div>
  );
};

export const TableKey = () => (
  <div className="w-full flex flex-wrap justify-center items-center text-xs mt-4">
    <p className="text-sm">Key (Percentile):</p>
    <div className="flex">
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
            "data p-1 ml-2 rounded lg:rounded-lg flex justify-center items-center"
          )}
        >
          {item.text}
        </span>
      ))}
    </div>
  </div>
);
