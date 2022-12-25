import React from "react";

import { round } from "../utils";
import { TeamYear } from "./types/api";

export const columnOptions = [
  { label: "Constant", accessor: (datum) => 1 },
  { label: "Auto EPA", accessor: (datum) => round(datum.auto_epa) },
  { label: "Teleop EPA", accessor: (datum) => round(datum.teleop_epa) },
  { label: "Endgame EPA", accessor: (datum) => round(datum.endgame_epa) },
  {
    label: "Auto + Endgame EPA",
    accessor: (datum) => round(datum.auto_epa + datum.endgame_epa),
  },
  { label: "RP 1 EPA", accessor: (datum) => round(datum.rp_1_epa, 3) },
  { label: "RP 2 EPA", accessor: (datum) => round(datum.rp_2_epa, 3) },

  { label: "Total EPA", accessor: (datum) => round(datum.total_epa) },
  { label: "Wins", accessor: (datum) => datum.wins },
  {
    label: "Win Rate",
    accessor: (datum) => round(datum.wins / (datum.wins + datum.losses + datum.ties), 3),
  },
  // For events
  { label: "Rank", accessor: (datum) => datum.rank },
  { label: "N - Rank", accessor: (datum) => datum.numTeams - datum.rank },
  { label: "RPs / Match", accessor: (datum) => round(datum.rps / datum.matches, 3) },
];

export const columnOptionsDict = columnOptions.reduce((acc, curr) => {
  acc[curr.label] = curr;
  return acc;
}, {});

export const ColumnBar = ({
  currColumnOptions,
  columns,
  setColumns,
}: {
  currColumnOptions: string[];
  columns: any;
  setColumns: any;
}) => {
  const columnKeys = Object.keys(columns);

  const smartSetColumns = (key: string, value: any) => {
    // Can add more logic here if needed
    setColumns({ ...columns, [key]: value });
  };

  return (
    <div className="flex flex-row items-center justify-center">
      {columnKeys.map((key) => (
        <div key={key} className="flex flex-col items-center justify-center">
          <p className="w-full pl-1 text-sm text-gray-500 capitalize">{key}-axis</p>
          <select
            className="border-2 border-gray-300 bg-white h-10 w-32 px-2 mr-2 rounded text-sm focus:outline-none appearance-none"
            onChange={(e) => smartSetColumns(key, e.target.value)}
            value={columns[key]}
          >
            {columnOptions
              .filter(
                (option) =>
                  currColumnOptions.includes(option.label) ||
                  (option.label === "Constant" && key === "z")
              )
              .map((option) => (
                <option key={option.label} value={option.label}>
                  {option.label}
                </option>
              ))}
          </select>
        </div>
      ))}
    </div>
  );
};
