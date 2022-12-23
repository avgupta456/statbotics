import React from "react";

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
