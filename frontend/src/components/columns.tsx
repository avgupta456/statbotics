import React from "react";
import Select from "react-select";

import { RP_NAMES } from "../constants";
import { APITeamEvent, APITeamYear } from "../types/api";
import { round } from "../utils";

type EYu = APITeamEvent | APITeamYear | undefined;
type Yu = APITeamYear | undefined;
type Eu = APITeamEvent | undefined;

export const getColumnOptions = (year: number) => [
  { label: "Constant", accessor: (datum: EYu) => 1 },
  {
    label: "Total EPA",
    accessor: (datum: EYu) => round(datum?.epa?.breakdown?.total_points),
  },
  {
    label: "Unitless EPA",
    accessor: (datum: EYu) => round(datum?.epa?.unitless, 0),
  },
  { label: "Norm EPA", accessor: (datum: EYu) => round(datum?.epa?.norm, 0) },
  ...(year >= 2016
    ? [
        {
          label: "Auto",
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.auto_points),
        },
        {
          label: "Teleop",
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.teleop_points),
        },
        {
          label: "Endgame",
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.endgame_points),
        },
        {
          label: "Auto + Endgame",
          accessor: (datum: EYu) =>
            round(datum?.epa?.breakdown?.auto_points + datum?.epa?.breakdown?.endgame_points),
        },
        {
          label: `${RP_NAMES[year][0]}`,
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.rp_1, 3),
        },
        {
          label: `${RP_NAMES[year][1]}`,
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.rp_2, 3),
        },
      ]
    : []),
  ...(year >= 2025
    ? [
        {
          label: `${RP_NAMES[year][2]}`,
          accessor: (datum: EYu) => round(datum?.epa?.breakdown?.rp_3, 3),
        },
      ]
    : []),
  { label: "Wins", accessor: (datum: Yu) => datum?.record?.wins },
  {
    label: "Win Rate",
    accessor: (datum: Yu) =>
      round(
        datum?.record?.wins / (datum?.record?.wins + datum?.record?.losses + datum?.record?.ties),
        3
      ),
  },
  // For events
  { label: "Rank", accessor: (datum: Eu) => datum?.record?.qual?.rank },
  { label: "RPs / Match", accessor: (datum: Eu) => round(datum?.record?.qual?.rps_per_match, 3) },
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
            className="w-28 md:w-36 text-sm mr-2 mb-4"
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
