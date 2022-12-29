"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { TeamMatch } from "../types/api";
import LineChart from "./Line";

const TeamLineChart = ({ teamNum, data }: { teamNum: number; data: TeamMatch[] }) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });

  // VARIABLES

  let teamData = {
    id: teamNum.toString(),
    data: data.map((teamMatch: any, i: number) => ({
      x: i,
      label: data[i - 1]?.label || "Start",
      y: teamMatch[yAxis.value],
    })),
  };

  // TODO: fix this to the actual post-match EPA
  const lastEPA = data[data.length - 1]?.[yAxis.value];
  teamData.data.push({ x: data.length, label: "End", y: lastEPA });

  // RENDER

  return (
    <div className="w-full flex flex-col">
      <div className="w-4/5 mx-auto flex flex-row justify-center">
        <Select
          instanceId={"y-axis-select"}
          className="flex-shrink-0 w-36 h-10 text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={[
            { value: "auto_epa", label: "Auto EPA" },
            { value: "teleop_epa", label: "Teleop EPA" },
            { value: "endgame_epa", label: "Endgame EPA" },
            { value: "total_epa", label: "Total EPA" },
            { value: "rp_1_epa", label: "RP 1 EPA" },
            { value: "rp_2_epa", label: "RP 2 EPA" },
          ]}
          onChange={(e: any) => setYAxis(e)}
          value={yAxis}
        />
      </div>
      <div className="flex">
        <LineChart
          data={[teamData]}
          xAxis="Match"
          yAxis={yAxis.label}
          isRP={yAxis.value.includes("rp_")}
        />
      </div>
    </div>
  );
};

export default TeamLineChart;
