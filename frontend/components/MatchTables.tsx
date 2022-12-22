import React from "react";

import { classnames } from "../utils";

export type Stats = {
  auto_mean: number;
  teleop_mean: number;
  endgame_mean: number;
  total_mean: number;
};

export const TeamLink = ({ team }: { team: string }) => (
  <a
    href={`/team/${team}`}
    target="_blank"
    rel="noopener noreferrer"
    className="text-blue-500 hover:text-blue-600 underline cursor-pointer"
  >
    {team}
  </a>
);

export const formatCell = (
  stats: Stats,
  info: any,
  multiplier: number = 1 / 3
) => {
  const row = info.row.original.name;
  const value = info.getValue();
  const mean =
    multiplier *
    (row === "Auto"
      ? stats.auto_mean
      : row === "Teleop"
      ? stats.teleop_mean
      : row === "Endgame"
      ? stats.endgame_mean
      : row === "Fouls"
      ? value // Fouls are not normalized
      : stats.total_mean);
  let color = "text-gray-800 bg-gray-200";
  if (value < 0.5 * mean) {
    color = "text-red-700 bg-red-300";
  }
  if (value > 1.5 * mean) {
    color = "text-green-500 bg-green-100";
  }
  if (value > 2 * mean) {
    color = "text-green-700 bg-green-300";
  }
  if (value > 3 * mean) {
    color = "text-black bg-green-500";
  }
  if (value > 4 * mean) {
    color = "text-blue-500 bg-blue-100";
  }
  if (value > 5 * mean) {
    color = "text-blue-700 bg-blue-300";
  }
  if (value > 6 * mean) {
    color = "text-white bg-blue-500";
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

export const headerClassName = (header: any) =>
  classnames(
    "w-24 py-2",
    header.colSpan > 1 ? "border-b-2" : "",
    header.id.includes("red") ? "bg-red-200" : "",
    header.id.includes("blue") ? "bg-blue-200" : "",
    header.id.includes("name") ? "bg-gray-50" : "",
    header.id === "redPred" || header.id === "red1" ? "rounded-tl-lg" : "",
    header.id === "bluePred" || header.id === "blue1" ? "rounded-tr-lg" : ""
  );

export const rowClassName = (row: any) =>
  classnames(
    "text-center h-full",
    row.index % 2 === 0 ? "bg-gray-50" : "",
    row.original.name === "Total"
      ? "font-bold bg-gray-300"
      : "hover:bg-gray-100"
  );

export const cellClassName = (cell: any) =>
  classnames(
    "w-24 py-2",
    ["redTotal", "blueTotal", "name"].includes(cell.column.id)
      ? "border-l-2 border-r-2"
      : ""
  );

export const TableKey = () => (
  <>
    <div className="w-full flex justify-center items-center text-xs mt-8">
      <p className="text-sm">Key (Multiples of Mean):</p>
      {[
        { color: "text-red-700 bg-red-300", text: "< 0.5" },
        {
          color: "text-gray-800 bg-gray-200",
          text: "0.5 - 1.5",
        },
        { color: "text-green-500 bg-green-100", text: "1.5 - 2" },
        { color: "text-green-700 bg-green-300", text: "2 - 3" },
        { color: "text-black bg-green-500", text: "3 - 4" },
        { color: "text-blue-500 bg-blue-100", text: "4 - 5" },
        { color: "text-blue-700 bg-blue-300", text: "5 - 6" },
        { color: "text-white bg-blue-500", text: "6+" },
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
    <div className="hidden lg:flex w-full justify-center items-center text-sm mt-4">
      Note: Nonlinear sum for alliance component predictions, see docs for more
      details!
    </div>
  </>
);
