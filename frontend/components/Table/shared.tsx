import React from "react";

import { classnames } from "../../utils";

export const TeamLink = ({ team, num }: { team: string | number; num: string | number }) => (
  <a
    href={`/team/${num}`}
    target="_blank"
    rel="noopener noreferrer"
    className="text-blue-500 hover:text-blue-600 underline cursor-pointer"
  >
    {team}
  </a>
);

export const CONDITIONAL_COLORS = [
  "text-red-700 bg-red-300",
  "text-gray-800 bg-gray-200",
  "text-green-500 bg-green-100",
  "text-green-700 bg-green-300",
  "text-black bg-green-500",
  "text-blue-500 bg-blue-100",
  "text-blue-700 bg-blue-300",
  "text-white bg-blue-500",
];

export const getColor = (value: number, mean: number) => {
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

export const getRPColor = (value: number, mean: number) => {
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
      Note: Nonlinear sum for alliance component predictions, see docs for more details!
    </div>
  </>
);
