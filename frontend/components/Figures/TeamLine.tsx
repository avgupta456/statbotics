"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { BACKEND_URL } from "../../constants";
import LineChart from "./Line";

const TeamLineChart = ({ teamNum, year }: { teamNum: number; year: number }) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });
  const [data, setData] = useState<any>([]);

  // FUNCTIONS

  useEffect(() => {
    const fetchData = async (teamNum: number) => {
      const res = await fetch(`${BACKEND_URL}/team_year/${year}/${teamNum}`);
      if (!res.ok) {
        return undefined;
      }

      const data = await res.json();
      if (!data) {
        console.log("No data found for team " + teamNum);
        return undefined;
      }

      const sortedData = data.data
        // .filter((teamMatch: any) => !teamMatch.playoff)
        .sort((a: any, b: any) => a.time - b.time);

      return sortedData;
    };

    fetchData(teamNum).then((data) => setData(data));
  }, [teamNum, year]);

  // VARIABLES

  console.log(data);

  const teamData = {
    id: teamNum.toString(),
    data: data.map((teamMatch: any, i: number) => ({
      x: i,
      label: teamMatch.match.toString(),
      y: teamMatch[yAxis.value],
    })),
  };

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
