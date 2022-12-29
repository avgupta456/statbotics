"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { TeamMatch } from "../types/api";
import LineChart from "./Line";

const TeamLineChart = ({
  teamNum,
  year,
  data,
}: {
  teamNum: number;
  year: number;
  data: TeamMatch[];
}) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });
  const [splitEvents, setSplitEvents] = useState(false);

  // VARIABLES

  let arr = data.map((teamMatch: any, i: number) => ({
    x: i,
    event: teamMatch.label.split("_")[0],
    label: data[i - 1]?.label || "Start",
    y: teamMatch[yAxis.value],
  }));

  // TODO: fix this to the actual post-match EPA
  const lastEPA = data[data.length - 1]?.[yAxis.value];
  const lastEvent = data[data.length - 1]?.label.split("_")[0];
  arr.push({ x: data.length, event: lastEvent, label: "End", y: lastEPA });

  let teamData = [
    {
      id: teamNum.toString(),
      data: arr,
    },
  ];

  if (splitEvents) {
    teamData = teamData[0].data.reduce((acc, curr) => {
      if (!acc[curr.event]) {
        acc[curr.event] = [];
      }
      acc[curr.event].push(curr);
      return acc;
    }, {} as any);

    teamData = Object.keys(teamData).map((event) => ({
      id: event,
      data: teamData[event],
    }));

    teamData = teamData.sort((a, b) => a.data[0].x - b.data[0].x);
  }

  // RENDER

  const yAxisOptions =
    year >= 2016
      ? [
          { value: "total_epa", label: "Total EPA" },
          { value: "norm_epa", label: "Norm EPA" },
          { value: "auto_epa", label: "Auto EPA" },
          { value: "teleop_epa", label: "Teleop EPA" },
          { value: "endgame_epa", label: "Endgame EPA" },
          { value: "rp_1_epa", label: "RP 1 EPA" },
          { value: "rp_2_epa", label: "RP 2 EPA" },
        ]
      : [
          { value: "total_epa", label: "EPA" },
          { value: "norm_epa", label: "Norm EPA" },
        ];

  return (
    <div className="w-full flex flex-col">
      <div className="w-4/5 mx-auto flex flex-row justify-center">
        <Select
          instanceId={"y-axis-select"}
          className="flex-shrink-0 w-36 h-10 text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={yAxisOptions}
          onChange={(e: any) => setYAxis(e)}
          value={yAxis}
        />
        <button
          className="flex-shrink-0 filter_button w-36"
          onClick={() => setSplitEvents(!splitEvents)}
        >
          {splitEvents ? "Combine Events" : "Split Events"}
        </button>
      </div>
      <div className="flex">
        <LineChart
          data={teamData}
          xAxis="Match"
          yAxis={yAxis.label}
          isRP={yAxis.value.includes("rp_")}
        />
      </div>
    </div>
  );
};

export default TeamLineChart;
