import React from "react";
import Select from "react-select";

import { RPMapping } from "../constants";
import { round } from "../utils";

export const getColumnOptions = (year: number) => [
  { label: "Constant", accessor: (datum) => 1 },
  { label: "Total EPA", accessor: (datum) => round(datum?.total_epa) },
  { label: "Norm EPA", accessor: (datum) => round(datum?.norm_epa, 0) },
  { label: "Auto", accessor: (datum) => round(datum?.auto_epa) },
  { label: "Teleop", accessor: (datum) => round(datum?.teleop_epa) },
  { label: "Endgame", accessor: (datum) => round(datum?.endgame_epa) },
  {
    label: "Auto + Endgame",
    accessor: (datum) => round(datum?.auto_epa + datum?.endgame_epa),
  },
  { label: `${RPMapping?.[year]?.[0]}`, accessor: (datum) => round(datum?.rp_1_epa, 3) },
  { label: `${RPMapping?.[year]?.[1]}`, accessor: (datum) => round(datum?.rp_2_epa, 3) },

  { label: "Wins", accessor: (datum) => datum?.wins },
  {
    label: "Win Rate",
    accessor: (datum) => round(datum?.wins / (datum?.wins + datum?.losses + datum?.ties), 3),
  },
  // For events
  { label: "Rank", accessor: (datum) => datum?.rank },
  { label: "N - Rank", accessor: (datum) => datum?.numTeams - datum?.rank },
  { label: "RPs / Match", accessor: (datum) => round(datum?.rps_per_match, 3) },
];

export const getColumnOptionsDict = (year: number) =>
  getColumnOptions(year).reduce((acc, curr) => {
    acc[curr.label] = curr;
    return acc;
  }, {});

export const ColumnBar = ({
  year,
  currColumnOptions,
  columns,
  setColumns,
}: {
  year: number;
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
          <Select
            instanceId={"column-select-" + key}
            className="w-28 md:w-36 text-sm mr-2"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={getColumnOptions(year)
              .filter(
                (option) =>
                  currColumnOptions.includes(option.label) ||
                  (option.label === "Constant" && key === "z")
              )
              .map((option) => ({
                value: option.label,
                label: option.label,
              }))}
            onChange={(e) => smartSetColumns(key, e?.value)}
            value={{
              value: columns[key],
              label: columns[key],
            }}
          />
        </div>
      ))}
    </div>
  );
};
